from typing import Optional, Any
from starlette import status
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from fastapi import Response


def success_response(
    message: str = "", data: Optional[Any] = None, status_code: int = 200
):
    if status_code == status.HTTP_204_NO_CONTENT:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return JSONResponse(
        status_code=status_code,
        content={"success": True, "message": message, "data": jsonable_encoder(data)},
    )


def error_response(
    message: str = "", data: Optional[Any] = None, status_code: int = 500
):
    return JSONResponse(
        status_code=status_code,
        content={"success": False, "message": message, "data": data},
    )
