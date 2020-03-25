from dynaconf import settings
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from pypis import __version__
from pypis.api.errors.http_error import http_error_handler
from pypis.api.errors.validation_error import http_422_error
from pypis.api.routes.api import router
from pypis.core.config import configure
from pypis.core.events import start_app_handler, stop_app_handler


def get_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME, debug=settings.FASTAPI.DEBUG, version=__version__
    )

    app.add_event_handler("startup", start_app_handler(app))
    app.add_event_handler("shutdown", stop_app_handler(app))

    app.add_exception_handler(RequestValidationError, http_422_error)
    app.add_exception_handler(HTTPException, http_error_handler)

    app.include_router(router, prefix=settings.FASTAPI.API_PREFIX)

    return app


configure()
app = get_app()
