from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.db import get_db
from sqlalchemy import select
from typing import TypeVar, Type
from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T", bound=DeclarativeBase)

class BaseRepository:
    model: Type[T]

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self._db = db

    def _without_trashed(self):
        return select(self.model).where(self.model.deleted_at == None)