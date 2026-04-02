import uuid
from uuid import UUID

from tenacity import sleep

from .base_repository import BaseRepository
from sqlalchemy import select, desc
from app.models.notebook import Notebook
from app.schemes.notebook_scheme import NotebookDto, NotebookUpdateDto


class NotebookRepository(BaseRepository):
    async def find_by_user_id(self, user_id: int):
        notebooks = await self._db.execute(select(Notebook).where(Notebook.user_id == user_id))

        return notebooks.scalars().all()

    async def find_by_uid_and_user_id(self, uid: UUID, user_id: int):
        notebook = await self._db.execute(
            select(Notebook).where(Notebook.uid == uid).where(Notebook.user_id == user_id))

        return notebook.scalar_one_or_none()

    async def create(self, dto: NotebookDto):
        notebook = Notebook(
            name=dto.name,
            uid=dto.uid,
            user_id=dto.user_id
        )

        self._db.add(notebook)

        await self._db.commit()
        await self._db.refresh(notebook)

        return notebook

    async def get_last_by_user_id(self, user_id: int):
        query = (
            select(Notebook)
            .where(Notebook.user_id == user_id)
            .order_by(desc(Notebook.created_at))
            .limit(1)
        )

        result = await self._db.execute(query)
        return result.scalar_one_or_none()

    async def update(self, db_notebook: Notebook, dto: NotebookUpdateDto):
        update_data = dto.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_notebook, field, value)

        await self._db.commit()

        return db_notebook