import uuid
from starlette import status
from .base_service import BaseService
from app.schemes.note_scheme import NoteDto, NoteUpdateRequest
from app.dependencies.repository_dependency import NoteRepositoryDep
from app.core.exceptions import AppException
from app.models import Note


class NoteService(BaseService):
    def __init__(self, repository: NoteRepositoryDep):
        self.repository = repository

    async def get_notes_by_notebook(self, notebook_id: int):
        notes = await self.repository.get_by_notebook_id(notebook_id)

        return notes

    async def get_note_details(self, note_id: int, notebook_id: int):
        note = await self.repository.find_by_id_and_notebook_id(note_id, notebook_id)

        if note is None:
            raise AppException(
                message="Qayd mavjud emas", status_code=status.HTTP_404_NOT_FOUND
            )

        return note

    async def create(self, notebook_id: int):
        note = await self.repository.create(
            NoteDto(
                title='Nomsiz qayd',
                content='',
                notebook_id=notebook_id
            )
        )

        return note

    async def update_note(self, note: Note, request: NoteUpdateRequest):
        note = await self.repository.update(note, request)

        return note

    async def delete_note(self, note: Note):
        await self.repository.delete(note)

        return None
