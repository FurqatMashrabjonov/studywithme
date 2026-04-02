from typing import Optional, Any

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

def success_response(message: str = "", data: Optional[Any] = None, status_code:int = 200):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": jsonable_encoder(data)
        }
    )

def error_response(message: str = "", data: Optional[Any] = None, status_code:int = 500):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": data
        }
    )