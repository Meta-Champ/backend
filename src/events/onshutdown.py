from loguru import logger


async def event() -> None:
    logger.info('Event started')
    logger.info('Event finished')
