from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.security_dependency import get_request_user
from app.dependencies.service_dependency import AuthServiceDep
from app.core.http import success_response
from app.schemes.auth_scheme import RegisterRequest, LoginRequest
from app.schemes.user_scheme import UserPublic

router = APIRouter()

@router.post('/register')
async def register(service: AuthServiceDep, request: RegisterRequest):
    result = await service.register(request)

    return success_response(data=result.model_dump())

@router.post('/login')
async def login(service: AuthServiceDep, request: LoginRequest):
    result = await service.login(request)

    return success_response(data=result.model_dump())

@router.post('/logout')
async def logout():
    pass

@router.get('/me')
async def me(user = Depends(get_request_user)):
    return success_response(data=UserPublic.model_validate(user))