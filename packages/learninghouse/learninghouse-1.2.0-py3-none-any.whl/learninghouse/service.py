from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from learninghouse import versions
from learninghouse.api import brain, configuration, docs
from learninghouse.api.errors import (LearningHouseException,
                                      learninghouse_exception_handler,
                                      validation_error_handler)
from learninghouse.api.middleware import CatchAllException, CustomHeader
from learninghouse.core.logging import initialize_logging, logger
from learninghouse.core.settings import service_settings

APP_REFERENCE = 'learninghouse.service:app'

STATIC_DIRECTORY = str(Path(__file__).parent / 'static')


def get_application() -> FastAPI:
    settings = service_settings()

    initialize_logging(settings.logging_level)

    application = FastAPI(**settings.fastapi_kwargs)
    application.include_router(brain.router)
    application.include_router(configuration.router)
    application.include_router(docs.router)
    application.include_router(docs.versions_router)

    application.add_exception_handler(
        RequestValidationError, validation_error_handler)
    application.add_exception_handler(
        LearningHouseException, learninghouse_exception_handler)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_middleware(CatchAllException)
    application.add_middleware(CustomHeader)
    application.add_middleware(
        uvicorn.middleware.proxy_headers.ProxyHeadersMiddleware)

    application.mount(
        '/static', StaticFiles(directory=STATIC_DIRECTORY), name='static')

    return application


app = get_application()


def run():
    settings = service_settings()
    logger.info(f'Running {settings.title} {versions.service}')
    logger.info(versions.libraries_versions)
    logger.info(f'Running in {settings.environment} mode')
    logger.info(f'Listening on {settings.host}:{settings.port}')
    logger.info(f'Configuration directory {settings.brains_directory}')
    logger.info(f'URL to OpenAPI file {settings.openapi_url}')

    if settings.environment == 'production':
        if settings.debug:
            logger.warning(
                'Debugging active. Recommendation: Do not use in production mode!')

        if settings.reload:
            logger.warning(
                'Reloading active. Recommendation: Do not use in production mode!')

    if settings.documentation_url is not None:
        logger.info(
            f'See interactive documentation {settings.documentation_url}')

    uvicorn.run(app=APP_REFERENCE, log_config=None,
                **settings.uvicorn_kwargs)
