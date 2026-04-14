from typing import List

from starlette import status
from .base_service import BaseService
from app.dependencies.repository_dependency import FlashcardRepositoryDep
from app.core.exceptions import AppException
from app.models import Flashcard
from app.schemes.flashcard_scheme import FlashcardDto


class FlashcardService(BaseService):
    def __init__(self, repository: FlashcardRepositoryDep):
        self.repository = repository

    async def get_flashcards_by_notebook_id(self, notebook_id: int):
        notes = await self.repository.get_by_notebook_id(notebook_id)

        return notes

    async def get_flashcard_details(self, note_id: int, notebook_id: int):
        note = await self.repository.find_by_id_and_notebook_id(note_id, notebook_id)

        if note is None:
            raise AppException(
                message="Qayd mavjud emas", status_code=status.HTTP_404_NOT_FOUND
            )

        return note

    async def create(self, notebook_id: int, title: str, cards: List):
        db_flashcard = await self.repository.create(
            FlashcardDto(
                title=title,
                notebook_id=notebook_id,
                cards=cards,
            )
        )

        return db_flashcard

    async def update_flashcard(self, flashcard: Flashcard):
        await self.repository.delete(flashcard)

        return None
