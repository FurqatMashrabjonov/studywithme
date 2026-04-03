import uuid

from fastapi import Depends
from app.models import Notebook
from .service_dependency import NotebookServiceDep
from .service_dependency import NoteServiceDep
from .security_dependency import get_request_user


async def get_valid_notebook(
        notebook_uid: uuid.UUID, service: NotebookServiceDep, user=Depends(get_request_user)
):
    notebook = await service.get_notebook_details(notebook_uid, user.id)

    return notebook


async def get_valid_note(
        service: NoteServiceDep,
        note_id: int,
        notebook: Notebook = Depends(get_valid_notebook),
):
    notebook = await service.get_note_details(note_id, notebook.id)

    return notebook
