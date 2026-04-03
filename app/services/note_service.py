import uuid
from starlette import status
from .base_service import BaseService
from app.schemes.notebook_scheme import NotebookDto
from app.dependencies.repository_dependency import NoteRepositoryDep
from app.core.exceptions import AppException
from app.schemes.notebook_scheme import NotebookUpdateRequest, NotebookUpdateDto


class NoteService(BaseService):
    def __init__(self, repository: NoteRepositoryDep):
        self.repository = repository

    async def get_notes_by_notebook(self, notebook_id: int):
        notebooks = await self.repository.get_by_notebook_uid(notebook_id)

        return notebooks

    async def get_notebook_details(self, uid: uuid.UUID, user_id: int):
        notebook = await self.repository.find_by_uid_and_user_id(uid, user_id)

        if notebook is None:
            raise AppException(
                message="Daftar mavjud emas", status_code=status.HTTP_404_NOT_FOUND
            )

        return notebook

    async def create(self, user_id: int):
        uid = uuid.uuid4()
        last_notebook = await self.repository.get_last_by_user_id(user_id=user_id)
        if last_notebook is None:
            notebook_id = 1
        else:
            notebook_id = last_notebook.id + 1

        notebook = await self.repository.create(
            NotebookDto(name=f"Yangi daftar {notebook_id}", user_id=user_id, uid=uid)
        )

        return notebook

    async def update_notebook(
        self, uid: uuid.UUID, user_id: int, request: NotebookUpdateRequest
    ):
        db_notebook = await self.repository.find_by_uid_and_user_id(
            uid=uid, user_id=user_id
        )

        if db_notebook is None:
            raise AppException(
                message="Daftar mavjud emas", status_code=status.HTTP_404_NOT_FOUND
            )

        notebook = await self.repository.update(
            db_notebook, NotebookUpdateDto(name=request.name)
        )

        return notebook

    async def delete_notebook(self, uid: uuid.UUID, user_id: int):
        notebook = await self.repository.find_by_uid_and_user_id(uid, user_id)

        if notebook is None:
            raise AppException(
                message="Daftar mavjud emas", status_code=status.HTTP_404_NOT_FOUND
            )

        await self.repository.delete(notebook)

        return None
