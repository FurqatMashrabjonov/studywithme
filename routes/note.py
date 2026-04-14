from fastapi import APIRouter
from fastapi import Depends
from starlette import status
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.core.http import success_response
from app.dependencies.security_dependency import get_request_user
from app.dependencies.service_dependency import NoteServiceDep, FlashcardServiceDep
from app.models import Notebook, Note
from app.schemes.flashcard_scheme import FlashcardListResource
from app.schemes.note_scheme import NoteListResource, NoteResource, NoteUpdateRequest
from app.dependencies.route_dependency import get_valid_notebook, get_valid_note

router = APIRouter()


@router.get("/")
async def index(
        service: NoteServiceDep,
        flashcard_service: FlashcardServiceDep,
        notebook: Notebook = Depends(get_valid_notebook)
):
    notes = await service.get_notes_by_notebook_id(notebook.id)
    notes_list = [NoteListResource.model_validate({**nb.__dict__, "type": "note"}) for nb in notes]

    flashcards = await flashcard_service.get_flashcards_by_notebook_id(notebook_id=notebook.id)
    flashcards_list = [NoteListResource.model_validate({**fc.__dict__, "type": "flashcard"}) for fc in flashcards]

    data = notes_list + flashcards_list

    return success_response(data=data, status_code=HTTP_200_OK)


@router.get("/{note_id}")
async def show(note: Note = Depends(get_valid_note)):
    return success_response(
        data=NoteResource.model_validate(note), status_code=HTTP_200_OK
    )


@router.post("/")
async def store(
        service: NoteServiceDep,
        notebook=Depends(get_valid_notebook)
):
    note = await service.create(notebook_id=notebook.id)

    return success_response(
        data=NoteResource.model_validate(note), status_code=HTTP_201_CREATED
    )


@router.put("/{note_id}")
async def update(
    service: NoteServiceDep,
    request: NoteUpdateRequest,
    note: Note = Depends(get_valid_note),
    user=Depends(get_request_user),
):
    note = await service.update_note(note=note, request=request)

    return success_response(
        data=NoteResource.model_validate(note)
    )

@router.delete("/{note_id}")
async def destroy(
        service: NoteServiceDep,
        note: Note = Depends(get_valid_note),
        user=Depends(get_request_user)
):
    await service.delete_note(note=note)
    return success_response(status_code=status.HTTP_204_NO_CONTENT)
