from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from .http422_error_handler import exception as http422_error_handler
from loguru import logger


async def configure_exceptions(application: FastAPI) -> None:
    logger.info('Configure RequestValidationError exception..')
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    logger.info('Exceptions configured!')
