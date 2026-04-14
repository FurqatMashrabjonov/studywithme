from sqlalchemy.orm import selectinload

from .base_repository import BaseRepository
from app.models import Flashcard, FlashcardItem
from datetime import datetime, timezone
from sqlalchemy import desc
from ..schemes.flashcard_scheme import FlashcardDto


class FlashcardRepository(BaseRepository):
    model = Flashcard
    async def get_by_notebook_id(self, notebook_id: int):
        notes = await self._db.execute(
            self._without_trashed()
            .where(self.model.notebook_id == notebook_id)
            .order_by(desc(self.model.created_at))
        )

        return notes.scalars().all()

    async def find_by_id_and_notebook_id(self, note_id: int, notebook_id: int):
        notes = await self._db.execute(
            self._without_trashed()
            .where(self.model.id == note_id, self.model.notebook_id == notebook_id)
            .options(selectinload(Flashcard.items))
        )

        return notes.scalar_one_or_none()

    async def create(self, dto: FlashcardDto):
        data = dto.model_dump()
        cards_data = data.pop("cards", [])

        flashcard = self.model(**data)

        for card in cards_data:
            item = FlashcardItem(**card)
            flashcard.items.append(item)


        self._db.add(flashcard)

        await self._db.commit()
        await self._db.refresh(flashcard)

        return flashcard

    async def delete(self, flashcard: Flashcard):
        flashcard.deleted_at = datetime.now(timezone.utc)

        await self._db.commit()

        return True
