import uuid
from uuid import UUID
from .base_repository import BaseRepository
from sqlalchemy import desc
from app.models import Note
from app.schemes.notebook_scheme import NotebookDto, NotebookUpdateDto
from datetime import datetime, timezone


class NoteRepository(BaseRepository):
    model = Note

    async def get_by_notebook_uid(self, notebook_id: int):
        notebooks = await self._db.execute(
            self._without_trashed().where(self.model.id == notebook_id)
        )

        return notebooks.scalars().all()

    async def find_by_id_and_notebook_id(self, note_id: int, notebook_id: int):
        notebooks = await self._db.execute(
            self._without_trashed()
            .where(
                self.model.id == note_id,
                self.model.notebook_id == notebook_id
            )
        )

        return notebooks.scalar_one_or_none()

    async def find_by_uid_and_user_id(self, uid: UUID, user_id: int):
        notebook = await self._db.execute(
            self._without_trashed().where(
                self.model.uid == uid, self.model.user_id == user_id
            )
        )

        return notebook.scalar_one_or_none()

    async def create(self, dto: NotebookDto):
        notebook = self.model(**dto.model_dump())

        self._db.add(notebook)

        await self._db.commit()
        await self._db.refresh(notebook)

        return notebook

    async def get_last_by_user_id(self, user_id: int):
        query = (
            self._without_trashed()
            .where(self.model.user_id == user_id)
            .order_by(desc(self.model.created_at))
            .limit(1)
        )

        result = await self._db.execute(query)
        return result.scalar_one_or_none()

    async def update(self, db_notebook: Note, dto: NotebookUpdateDto):
        update_data = dto.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_notebook, field, value)

        await self._db.commit()

        return db_notebook

    async def delete(self, notebook: Note):
        notebook.deleted_at = datetime.now(timezone.utc)

        await self._db.commit()

        return True
