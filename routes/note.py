import uuid
from fastapi import APIRouter
from fastapi import Depends

from starlette import status
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.core.http import success_response
from app.dependencies.security_dependency import get_request_user
from app.dependencies.service_dependency import NoteServiceDep
from app.schemes.note_scheme import NoteListResource, NoteResource, NoteUpdateRequest

router = APIRouter()


@router.get("/")
async def index(notebook_uid, service: NoteServiceDep, user=Depends(get_request_user)):
    notes = await service.get_user_notes(user.id)
    data = [NoteListResource.model_validate(nb) for nb in notes]

    return success_response(data=data, status_code=HTTP_200_OK)


@router.get("/{id}")
async def show(id: int, service: NoteServiceDep, user=Depends(get_request_user)):
    note = await service.get_note_details(id, user.id)

    return success_response(
        data=NoteResource.model_validate(note), status_code=HTTP_200_OK
    )


@router.post("/")
async def store(service: NoteServiceDep, user=Depends(get_request_user)):
    note = await service.create(user.id)

    return success_response(
        data=NoteResource.model_validate(note), status_code=HTTP_201_CREATED
    )


@router.put("/{uid}")
async def update(
    service: NoteServiceDep,
    request: NoteUpdateRequest,
    user=Depends(get_request_user),
):
    pass


@router.delete("/{uid}")
async def destroy(service: NoteServiceDep, user=Depends(get_request_user)):

    return success_response(status_code=status.HTTP_204_NO_CONTENT)
