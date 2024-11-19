from src.core.database import get_async_session
from src.core.schema import (
    Person as PersonSchema,
    Address as AddressSchema,
    Passport as PassportSchema
)
from src.middlewares import authenticate
from src.models.person import Person, PersonInternal
from src.models.address import Address
from src.models.passport import Passport
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __403__, __404__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
persons = FastCRUD(PersonSchema)
addresses = FastCRUD(AddressSchema)
passports = FastCRUD(PassportSchema)


@router.get(
    path='/{id}',
    response_model=Person,
    responses={
        403: __403__,
        404: __404__,
        500: __500__,
    },
    status_code=200,
    summary='Получение персоны',
    response_description='Персона получена',
)
async def request(
    id: int,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Person | HTTPException:
    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN]:
        raise HTTPException(status_code=403, detail='Access denied')

    row: PersonInternal | None = await persons.get(
        conn,
        id=id,
        schema_to_select=PersonInternal,
        return_as_model=True
    )

    if not row:
        raise HTTPException(status_code=404, detail='Персона не найдена')

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
