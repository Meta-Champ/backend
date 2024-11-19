from src.core.database import get_async_session
from src.core.schema import (
    Person as PersonSchema,
    Address as AddressSchema,
    Passport as PassportSchema
)
from src.middlewares import authenticate
from src.models.person import Person, PersonInternal, PersonDump
from src.models.address import AddressInternal
from src.models.passport import PassportInternal
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __403__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
persons = FastCRUD(PersonSchema)
addresses = FastCRUD(AddressSchema)
passports = FastCRUD(PassportSchema)


@router.get(
    path='/',
    response_model=PersonDump,
    responses={
        403: __403__,
        500: __500__,
    },
    status_code=200,
    summary='Получение персон',
    response_description='Персоны получены',
)
async def request(
    offset: int = 0,
    limit: int = 100,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> PersonDump | HTTPException:
    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN]:
        raise HTTPException(status_code=403, detail='Access denied')

    if offset < 0:
        raise HTTPException(status_code=400, detail='Значение offset не может быть меньше 0')
    
    if limit < 1:
        raise HTTPException(status_code=400, detail='Значение limit не может быть меньше 1')

    if limit > 100:
        raise HTTPException(status_code=400, detail='Значение limit не может быть больше 100')

    rows: list[PersonInternal] = await persons.get_multi(
        conn,
        offset=offset,
        limit=limit,
        schema_to_select=PersonInternal,
        return_as_model=True
    )

    if not rows:
        raise HTTPException(status_code=404, detail='Персоны не найдены')

    address_ids = [row.address_id for row in rows['data']]
    passport_ids = [row.passport_id for row in rows['data']]

    addresses_dict = {address.id: address for address in (await addresses.get_multi(
        conn,
        ids=address_ids,
        schema_to_select=AddressInternal,
        return_as_model=True
    ))['data']}

    passports_dict = {passport.id: passport for passport in (await passports.get_multi(
        conn,
        ids=passport_ids,
        schema_to_select=PassportInternal,
        return_as_model=True
    ))['data']}


    for row in rows:
        print(row)

    _persons = [
        Person(**{
            **row.model_dump(),
            'address': addresses_dict.get(row.address_id),
            'passport': passports_dict.get(row.passport_id)
        }) for row in rows['data']
    ]

    return PersonDump(
        data=_persons,
        total_count=len(_persons)
    )
