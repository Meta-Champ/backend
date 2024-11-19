from src.core.database import get_async_session
from src.core.schema import (
    Person as PersonSchema,
    Address as AddressSchema,
    Passport as PassportSchema
)
from src.middlewares import authenticate
from src.models.person import Person, PersonUpdate, PersonInternal
from src.models.address import Address
from src.models.passport import Passport
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __400__, __403__, __404__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
persons = FastCRUD(PersonSchema)
addresses = FastCRUD(AddressSchema)
passports = FastCRUD(PassportSchema)


@router.patch(
    path='/{id}',
    response_model=Person,
    responses={
        400: __400__,
        403: __403__,
        404: __404__,
        500: __500__,
    },
    status_code=200,
    summary='Обновление персоны',
    response_description='Персона обновлена',
)
async def request(
    id: int, 
    data: PersonUpdate,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Person | HTTPException:
    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN]:
        raise HTTPException(status_code=403, detail='Access denied')

    row: PersonInternal | None = await persons.get(
        conn,
        id = id,
        schema_to_select=PersonInternal,
        return_as_model=True
    )

    if not row:
        raise HTTPException(status_code=404, detail='Персона не найдена')

    if data.address is not None:
        await addresses.update(
            db=conn,
            id=row.address_id,
            object=Address(**(data.address.model_dump()))
        )

    if data.passport is not None:
        await passports.update(
            db=conn,
            id=row.passport_id,
            object=Passport(**(data.passport.model_dump()))
        )

    obj = {}

    if data.first_name is not None:
        obj['first_name'] = data.first_name

    if data.middle_name is not None:
        obj['middle_name'] = data.middle_name

    if data.last_name is not None:
        obj['last_name'] = data.last_name

    if data.email is not None:
        obj['email'] = data.email

    if data.phone is not None:
        obj['phone'] = data.phone

    if data.snils is not None:
        obj['snils'] = data.snils

    await persons.update(db=conn, id=id, object=obj)

    row: PersonInternal = await persons.get(
        conn,
        id = id,
        schema_to_select=PersonInternal,
        return_as_model=True
    )

    return Person(**{
        **row.model_dump(),
        'address': await addresses.get(
            conn,
            id=row.address_id,
            schema_to_select=Address,
            return_as_model=True
        ),
        'passport': await passports.get(
            conn,
            id=row.passport_id,
            schema_to_select=Passport,
            return_as_model=True
        )
    })
