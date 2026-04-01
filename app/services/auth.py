from .base import BaseService
from app.schemes.auth import RegisterRequest, RegisterResponse
from app.core.security import create_access_token
from app.schemes.api import success_response
from app.dependencies.service import UserServiceDep

class AuthService(BaseService):
    async def register(self, data: RegisterRequest, user_service: UserServiceDep):
        user_model = await user_service.create_user(data)
        token = create_access_token(user_model.id)

        return success_response(
            message="User created and registered",
            data=RegisterResponse(
                access_token=token
            )
        )