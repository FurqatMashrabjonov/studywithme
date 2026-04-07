import uuid
from uuid import UUID
from .base_repository import BaseRepository
from sqlalchemy import desc
from app.models import Note
from app.schemes.note_scheme import NoteDto, NoteUpdateRequest
from datetime import datetime, timezone


class NoteRepository(BaseRepository):
    model = Note

    async def get_by_notebook_id(self, notebook_id: int):
        notes = await self._db.execute(
            self._without_trashed().where(self.model.notebook_id == notebook_id)
        )

        return notes.scalars().all()

    async def find_by_id_and_notebook_id(self, note_id: int, notebook_id: int):
        notes = await self._db.execute(
            self._without_trashed().where(
                self.model.id == note_id, self.model.notebook_id == notebook_id
            )
        )

        return notes.scalar_one_or_none()

    async def create(self, dto: NoteDto):
        note = self.model(**dto.model_dump())

        self._db.add(note)

        await self._db.commit()
        await self._db.refresh(note)

        return note

    async def update(self, db_note: Note, dto: NoteUpdateRequest):
        update_data = dto.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_note, field, value)

        await self._db.commit()

        return db_note

    async def delete(self, note: Note):
        note.deleted_at = datetime.now(timezone.utc)

        await self._db.commit()

        return True
