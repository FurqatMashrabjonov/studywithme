from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.db import get_db

class BaseRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self._db = db