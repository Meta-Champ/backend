from src.core.database import get_async_session
from src.core.schema import User as UserSchema
from src.middlewares import authenticate
from src.models.user import UserExternal
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __403__, __404__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
users = FastCRUD(UserSchema)


@router.get(
    path='/{id}',
    response_model=UserExternal,
    responses={
        403: __403__,
        404: __404__,
        500: __500__,
    },
    status_code=200,
    summary='Получение пользователя',
    response_description='Пользователь получен',
)
async def request(
    id: int,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> UserExternal | HTTPException:
    user_id = id

    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN]:
        user_id = user.id

    row: UserExternal | None = await users.get(
        conn,
        id=user_id,
        schema_to_select=UserExternal,
        return_as_model=True
    )

    if not row:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    return row
