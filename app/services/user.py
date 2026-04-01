from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from .base import BaseService
from app.schemes.auth import RegisterRequest
from app.models import User
from app.core.security import hash_password
from sqlalchemy import select

class UserService(BaseService):
    async def create_user(self, data: RegisterRequest):
        db_user = await self.get_user_by_email(data.email)

        if db_user is not None:
            raise Exception(f"User with [{data.email}] already exists")

        user = User(
            name=data.name,
            email=data.email,
            password=hash_password(data.password)
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def get_user_by_email(self, email: str):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()