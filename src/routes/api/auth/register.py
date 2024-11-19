from src.core.database import get_async_session
from src.core.schema import User as UserSchema
from src.core.settings import settings
from src.models.auth import AuthRegister, AuthTokens
from src.models.user import UserCreateInternal, User
from src.models.role import SystemRoles
from src.utils.jwt import generate_tokens
from src.utils.documentation_statuses import __400__, __500__

from fastapi import APIRouter, Depends, HTTPException, Response
from fastcrud import FastCRUD
from passlib.context import CryptContext
from loguru import logger
import secrets


router = APIRouter()
user = FastCRUD(UserSchema)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post(
    path='/register',
    response_model=AuthTokens,
    responses={
        400: __400__,
        500: __500__,
    },
    status_code=200,
    summary='Регистрация',
    response_description='Регистрация прошла успешно',
)
async def request(
    data: AuthRegister,
    response: Response,
    conn = Depends(get_async_session)
) -> AuthTokens | HTTPException:
    logger.info(f'New register request: username={data.username}')

    _user: User | None = await user.get(
        db=conn,
        username=data.username,
        schema_to_select=User,
        return_as_model=True
    )

    if data.password != data.password_confirm:
        logger.info(f'User with username={data.username} has wrong password confirmation..')
        raise HTTPException(
            status_code=400,
            detail='Пароли не совпадают'
        )

    if _user:
        logger.info(f'User with username={data.username} already exists..')
        raise HTTPException(
            status_code=400,
            detail='Пользователь с таким логином уже зарегистрирован'
        )
    
    password_salt = secrets.token_hex(8)

    new_user = await user.create(
        conn,
        object=UserCreateInternal(
            username=data.username,
            password=pwd_context.hash(f'{data.password}{password_salt}'),
            password_salt=password_salt,
            role=SystemRoles.USER
        ),
    )

    logger.info(f'User with username={data.username} has been created..')

    tokens = await generate_tokens(new_user.id)

    response.set_cookie(key='access_token', value=tokens.access_token, expires=86_400 * settings.security.JWT_ACCESS_TOKEN_ALIVE_IN_DAYS)
    response.set_cookie(key='refresh_token', value=tokens.refresh_token, expires=86_400 * settings.security.JWT_REFRESH_TOKEN_ALIVE_IN_DAYS)

    return tokens
