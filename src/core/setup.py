from collections.abc import AsyncGenerator, Callable
from contextlib import _AsyncGeneratorContextManager, asynccontextmanager
from typing import Any
from loguru import logger
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from fastapi import APIRouter, FastAPI

from .settings import Settings
from src.events import configure_events
from src.exceptions import configure_exceptions


def lifespan_factory() -> Callable[[FastAPI], _AsyncGeneratorContextManager[Any]]:
    logger.info('Lifespan entry')

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncGenerator:
        logger.info('Add event handlers..')
        await configure_events(application)
        
        logger.info('Add exceptions handlers..')
        await configure_exceptions(application)
        yield

    return lifespan


def create_application(
    router: APIRouter,
    settings: Settings,
    **kwargs: Any,
) -> FastAPI:
    logger.info('Create application..')
    logger.info('Configure app settings..')

    kwargs.update({
        'title': settings.docs.APP_NAME,
        'description': None,
        'openapi_url': settings.docs.OPENAPI_PATH,
        'docs_url': settings.docs.SWAGGER_PATH,
        'redoc_url': settings.docs.REDOC_PATH,
    })

    logger.info('Init FastAPI..')
    application = FastAPI(
        lifespan=lifespan_factory(),
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        ],
        **kwargs
    )

    logger.info('Add routes..')
    application.include_router(router)

    logger.info('Application successfully created!')
    return application
