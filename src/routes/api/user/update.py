from src.core.database import get_async_session
from src.core.schema import User as UserSchema
from src.middlewares import authenticate
from src.models.user import User, UserUpdate
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __400__, __403__, __404__, __409__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD
from passlib.context import CryptContext

router = APIRouter()
users = FastCRUD(UserSchema)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.patch(
    path='/{id}',
    response_model=User,
    responses={
        400: __400__,
        403: __403__,
        404: __404__,
        409: __409__,
        500: __500__,
    },
    status_code=200,
    summary='Обновление пользователя',
    response_description='Пользователь обновлен',
)
async def request(
    id: int, 
    data: UserUpdate,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> User | HTTPException:
    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN]:
        raise HTTPException(status_code=403, detail='Access denied')

    row: User | None = await users.get(
        conn,
        id = id,
        schema_to_select=User,
        return_as_model=True
    )

    if not row:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    obj = {}

    if data.person_id is not None:
        if not await users.exists(conn, id__ne=id, person_id=data.person_id):
            raise HTTPException(status_code=409, detail='Персона с таким идентификатором уже занята')
        
        obj['person_id'] = data.person_id

    if data.role is not None:
        if data.role not in [SystemRoles.USER, SystemRoles.ADMIN] or \
            (user.role == SystemRoles.OWNER and data.role != SystemRoles.OWNER):
            raise HTTPException(status_code=400, detail='Недопустимая роль')
        
        obj['role'] = data.role

    if data.username is not None:
        if await users.exists(conn, id__ne=id, username=data.username):
            raise HTTPException(status_code=409, detail='Пользователь с таким именем уже существует')
        
        obj['username'] = data.username

    if data.password is not None:
        obj['password'] = pwd_context.hash(f'{data.password}{row.password_salt}')

    await users.update( db=conn, id = id, object=obj)

    return User(**{**row, **obj})
