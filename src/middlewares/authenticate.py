from src.core.database import get_async_session
from src.core.schema import User as UserSchema
from src.core.settings import settings
from src.models.user import User
from src.utils.jwt import generate_tokens

from typing import Annotated
from fastapi import Depends, HTTPException, Request, Response
from fastapi.security import HTTPBearer
from fastcrud import FastCRUD
from jose import JWTError, jwt, ExpiredSignatureError
import time

security = HTTPBearer()
user = FastCRUD(UserSchema)


async def check(
    request: Request,
    response: Response,
    token: Annotated[str, Depends(security)],
    conn = Depends(get_async_session)
):
    credentials_exception = HTTPException(status_code=401, detail='Не авторизован')

    user_id: int | None = None

    try:
        payload = jwt.decode(
            token.credentials,
            settings.security.JWT_SECRET,
            algorithms=[settings.security.JWT_ALGORITHM]
        )

        user_id = int(payload.get('sub'))

        if payload.get('token_type') != 'access':
            raise credentials_exception
    except ExpiredSignatureError:
        try:
            payload = jwt.decode(
                request.cookies.get('refresh_token'),
                settings.security.JWT_SECRET,
                algorithms=[settings.security.JWT_ALGORITHM]
            )

            user_id = int(payload.get('sub'))

            if payload.get('token_type') != 'refresh':
                raise credentials_exception
            
            tokens = await generate_tokens(user_id=user_id)

            response.set_cookie(key='access_token', value=tokens.access_token, expires=86_400 * settings.security.JWT_ACCESS_TOKEN_ALIVE_IN_DAYS)
            response.set_cookie(key='refresh_token', value=tokens.refresh_token, expires=86_400 * settings.security.JWT_REFRESH_TOKEN_ALIVE_IN_DAYS)
        except JWTError as e:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception

    finded_user: User | None = await user.get(
        conn,
        id=user_id,
        schema_to_select=User,
        return_as_model=True
    )

    if not finded_user:
        raise credentials_exception

    return finded_user
