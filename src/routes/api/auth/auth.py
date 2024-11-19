from src.core.database import get_async_session
from src.core.schema import User as UserSchema
from src.core.settings import settings
from src.models.auth import AuthLogin, AuthTokens
from src.models.user import User
from src.utils.jwt import generate_tokens
from src.utils.documentation_statuses import __401__, __500__

from fastapi import APIRouter, Depends, HTTPException, Response
from fastcrud import FastCRUD
from passlib.context import CryptContext
from loguru import logger


router = APIRouter()
user = FastCRUD(UserSchema)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post(
    path='/login',
    response_model=AuthTokens,
    responses={
        401: __401__,
        500: __500__,
    },
    status_code=200,
    summary='Авторизация',
    response_description='Авторизация прошла успешно',
)
async def request(
    data: AuthLogin,
    response: Response,
    conn = Depends(get_async_session)
) -> AuthTokens | HTTPException:
    not_authorize = HTTPException(
        status_code=401,
        detail='Неверный логин или пароль'
    )

    logger.info(f'New auth login request: username={data.username}')

    _user: User | None = await user.get(
        db=conn,
        username=data.username,
        schema_to_select=User,
        return_as_model=True
    )

    if _user is None:
        logger.info(f'User with username={data.username} not exists..')
        raise not_authorize
    
    if not pwd_context.verify(f'{data.password}{_user.password_salt}', _user.password):
        logger.info(f'User with username={data.username} has wrong password..')
        raise not_authorize

    tokens = await generate_tokens(_user.id)

    response.set_cookie(key='access_token', value=tokens.access_token, expires=86_400 * settings.security.JWT_ACCESS_TOKEN_ALIVE_IN_DAYS)
    response.set_cookie(key='refresh_token', value=tokens.refresh_token, expires=86_400 * settings.security.JWT_REFRESH_TOKEN_ALIVE_IN_DAYS)

    return tokens
