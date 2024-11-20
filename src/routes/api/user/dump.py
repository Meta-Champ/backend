from src.core.database import get_async_session
from src.core.schema import User as UserSchema
from src.middlewares import authenticate
from src.models.user import UserExternal, UserDump
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __403__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
users = FastCRUD(UserSchema)


@router.get(
    path='/',
    response_model=UserDump,
    responses={
        403: __403__,
        500: __500__,
    },
    status_code=200,
    summary='Получение пользователей',
    response_description='Пользователи получены',
)
async def request(
    offset: int = 0,
    limit: int = 100,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> UserDump | HTTPException:
    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN]:
        raise HTTPException(status_code=403, detail='Access denied')
    
    if offset < 0:
        raise HTTPException(status_code=400, detail='Значение offset не может быть меньше 0')
    
    if limit < 1:
        raise HTTPException(status_code=400, detail='Значение limit не может быть меньше 1')

    if limit > 100:
        raise HTTPException(status_code=400, detail='Значение limit не может быть больше 100')
    
    return await users.get_multi(
        conn,
        offset=offset,
        limit=limit,
        schema_to_select=UserExternal,
        return_as_model=True
    )
