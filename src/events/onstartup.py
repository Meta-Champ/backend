from src.core.database import get_async_session
from loguru import logger
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def event() -> None:
    logger.info('Event started')

    logger.info('Check users exists')
    await check_users_exists()

    logger.info('Event finished')


async def check_users_exists():
    db = await anext(get_async_session())
    users_count = 0 # TODO: db get 'users' 

    if not users_count:
        logger.warning("Admin user not found, create account..")
        # create user
        logger.warning("Admin user created! Username=metaadmin, password=metapass.")
