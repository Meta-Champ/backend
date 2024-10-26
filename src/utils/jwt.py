from src.core.settings import settings
from src.models.auth import AuthTokens

from jose import jwt

import time
import uuid

async def generate_tokens(user_id: int) -> AuthTokens:
    ts = int(time.time())
    token_id = str(uuid.uuid4())

    return AuthTokens(
        access_token=jwt.encode(
            {
                'jti': token_id,
                'sub': str(user_id),
                'iat': ts,
                'exp': ts + (settings.security.JWT_ACCESS_TOKEN_ALIVE_IN_DAYS * 86_400),
                'typ': 'Bearer',
                'token_type': 'access'
            },
            settings.security.JWT_SECRET,
            algorithm=settings.security.JWT_ALGORITHM
        ),
        refresh_token=jwt.encode(
            {
                'jti': token_id,
                'sub': str(user_id),
                'iat': ts,
                'token_type': 'refresh',
                'exp': ts + (settings.security.JWT_REFRESH_TOKEN_ALIVE_IN_DAYS * 86_400)
            },
            settings.security.JWT_SECRET,
            algorithm=settings.security.JWT_ALGORITHM
        )
    )
