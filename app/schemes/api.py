from typing import Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[T] = None



def success_response(message: str, data: Optional[T] = None):
    return ApiResponse(success=True, message=message, data = data)

def error_response(message: str, data: Optional[T] = None):
    return ApiResponse(success=False, message=message, data = data)