from src.core.database import get_async_session
from src.core.schema import User
from src.models.user import UserCreateInternal
from src.models.role import SystemRoles
from passlib.context import CryptContext
from fastcrud import FastCRUD
from loguru import logger
import secrets

user = FastCRUD(User)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def event() -> None:
    logger.info('Event started')

    logger.info('Check users exists')
    await check_owner_exists()

    logger.info('Event finished')


async def check_owner_exists(db = get_async_session()):
    db = await anext(db)

    owner = await user.count(db, role=SystemRoles.OWNER)

    if not owner:
        logger.warning("Owner user not found, create account..")
        
        password_salt = secrets.token_hex(8)

        await user.create(db, object=UserCreateInternal(
            username='metaadmin',
            password=pwd_context.hash(f'metapass{password_salt}'),
            password_salt=password_salt,
            role=SystemRoles.OWNER
        ))

        logger.warning("Owner user created! Username=metaadmin, password=metapass.")
