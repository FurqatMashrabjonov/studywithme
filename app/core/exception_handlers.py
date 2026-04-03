from fastapi import Request
from app.core.exceptions import AppException
from app.core.http import error_response


async def app_exception_handler(request: Request, exc: AppException):
    return error_response(status_code=exc.status_code, message=exc.message)
