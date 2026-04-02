from starlette import status
from .base_service import BaseService
from app.schemes.auth_scheme import (
    RegisterRequest,
    TokenResponse,
    LoginRequest
)
from app.core.security import create_access_token, verify_password
from app.dependencies.repository_dependency import UserRepositoryDep
from app.schemes.user_scheme import UserCreateDto
from app.core.exceptions import AppException


class AuthService(BaseService):
    def __init__(self, repository: UserRepositoryDep):
        self.repository = repository

    async def register(self, request: RegisterRequest) -> TokenResponse:
        db_user = await self.repository.get_user_by_email(request.email)

        if db_user is not None:
            raise AppException(f"Foydalanuvchi bu email bilan allaqachon mavjud", status_code=status.HTTP_409_CONFLICT)

        user = await self.repository.create(UserCreateDto.model_validate(request))
        token, expires_at = create_access_token(user.id)

        return TokenResponse(access_token=token, expires_at=expires_at)

    async def login(self, request: LoginRequest) -> TokenResponse:
        user = await self.repository.get_user_by_email(request.email)

        if user is None:
            raise AppException(f"Bu email bilan foydalanuchi mavjud emas", status_code=status.HTTP_409_CONFLICT)

        if not verify_password(request.password, user.password):
            raise AppException(f"Parol noto'g'ri", status_code=status.HTTP_409_CONFLICT)

        token, expires_at = create_access_token(user.id)

        return TokenResponse(access_token=token, expires_at=expires_at)

    async def logout(self):
        """
            1. get auth user and logout it. if it doesn't exist then raise error
        """

    async def me(self):
        pass