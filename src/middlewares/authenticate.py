from src.core.database import get_db
from src.core.settings import settings
from src.utils.jwt import generate_tokens

from typing import Annotated
from fastapi import Depends, HTTPException, Request, Response
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
import time

security = HTTPBearer()
db = get_db()


async def check(request: Request, response: Response, token: Annotated[str, Depends(security)]):
    credentials_exception = HTTPException(status_code=401, detail='Could not validate credentials')

    user_id: int | None = None
    expire: int | None = None

    try:
        payload = jwt.decode(
            token.credentials,
            settings.security.JWT_SECRET,
            algorithms=[settings.security.JWT_ALGORITHM]
        )

        user_id = int(payload.get('sub'))
        expire = int(payload.get('exp'))

        if payload.get('token_type') != 'access':
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception

    user = {} # TODO: db user find 

    if user_id != user['value']:
        raise credentials_exception

    tokens = await generate_tokens(user_id=user_id)

    if expire - time.time() < 10_000:
        response.set_cookie(key='access_token', value=tokens.access_token, expires=86_400 * settings.security.JWT_ACCESS_TOKEN_ALIVE_IN_DAYS)
        response.set_cookie(key='refresh_token', value=tokens.refresh_token, expires=86_400 * settings.security.JWT_REFRESH_TOKEN_ALIVE_IN_DAYS)

    return True
