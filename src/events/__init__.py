from fastapi import FastAPI
from .onstartup import event as onstartup
from loguru import logger


async def configure_events(application: FastAPI) -> None:
    logger.info('Configure OnStartup event..')
    application.add_event_handler('startup', await onstartup())

    logger.info('Events configured!')
