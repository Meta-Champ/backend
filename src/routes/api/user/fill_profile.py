from src.core.database import get_async_session
from src.core.schema import (
    Person as PersonSchema,
    Address as AddressSchema,
    Passport as PassportSchema,
    User as UserSchema
)
from src.middlewares import authenticate
from src.models.person import Person, PersonCreate, PersonInternalCreate
from src.models.address import Address, AddressInternal
from src.models.passport import Passport, PassportInternal
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __400__, __403__, __409__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()

persons = FastCRUD(PersonSchema)
addresses = FastCRUD(AddressSchema)
passports = FastCRUD(PassportSchema)
users = FastCRUD(UserSchema)


@router.put(
    path='/fillProfile',
    response_model=Person,
    responses={
        400: __400__,
        403: __403__,
        500: __500__,
    },
    status_code=200,
    summary='Заполнение профиля',
    response_description='Профиль заполнен',
)
async def request(
    data: PersonCreate,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Person | HTTPException:
    if user.person_id is not None:
        raise HTTPException(status_code=400, detail='Профиль уже заполнен')

    address: AddressInternal = await addresses.create(
        db=conn,
        object=Address(**(data.address.model_dump()))
    )

    passport: PassportInternal = await passports.create(
        db=conn,
        object=Passport(**(data.passport.model_dump()))
    )

    obj = {
        **data.model_dump(),
        'address_id': address.id,
        'passport_id': passport.id
    }

    to_create = PersonInternalCreate(**obj)

    person = await persons.create(
        db=conn,
        object=to_create
    )

    await users.update(
        db=conn,
        id=user.id,
        object={'person_id': person.id}
    )

    return Person(**{
        'id': person.id,
        **to_create.model_dump(),
        'address': data.address.model_dump(),
        'passport': data.passport.model_dump()
    })
