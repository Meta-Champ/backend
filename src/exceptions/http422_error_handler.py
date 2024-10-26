from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def exception(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={ 'detail': [ exc.detail ] }
    )
