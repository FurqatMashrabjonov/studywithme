from fastapi import APIRouter, Body
from app.dependencies.service import AuthServiceDep
from app.schemes.auth import RegisterRequest

router = APIRouter()


@router.post('/login')
def login():
    pass

@router.post('/register')
async def register(service: AuthServiceDep, data: RegisterRequest):
    return await service.register(data)

@router.get('/me')
def me():
    pass