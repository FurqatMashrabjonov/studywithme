from .base_repository import BaseRepository
from sqlalchemy import select
from app.models import User
from app.core.security import hash_password
from app.schemes.user_scheme import UserCreateDto


class UserRepository(BaseRepository):
    model = User

    async def create(self, dto: UserCreateDto):
        user = self.model(
            name=dto.name,
            email=dto.email,
            password=hash_password(dto.password),
        )

        self._db.add(user)
        await self._db.commit()
        await self._db.refresh(user)

        return user

    async def get_user_by_email(self, email: str):
        result = await self._db.execute(
            self._without_trashed().where(self.model.email == email)
        )

        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int):
        result = await self._db.execute(
            self._without_trashed().where(self.model.id == user_id)
        )

        return result.scalar_one_or_none()
