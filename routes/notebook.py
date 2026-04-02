from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from starlette import status
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.core.http import success_response
from app.dependencies.security_dependency import get_request_user
from app.dependencies.service_dependency import NotebookServiceDep
from app.schemes.notebook_scheme import NotebookUpdateRequest, NotebookPublic

router = APIRouter()


@router.get('/')
async def index(service: NotebookServiceDep, user=Depends(get_request_user)):
    """
       Don't forget to add pagination
    """
    notebooks = await service.get_user_notebooks(user.id)
    data = [NotebookPublic.model_validate(nb) for nb in notebooks]

    return success_response(data=data, status_code=HTTP_200_OK)


@router.get('/{uid}')
async def show(uid: UUID, service: NotebookServiceDep, user=Depends(get_request_user)):
    notebook = await service.get_notebook_details(uid, user.id)

    return success_response(data=NotebookPublic.model_validate(notebook), status_code=HTTP_200_OK)


@router.post('/')
async def store(service: NotebookServiceDep, user=Depends(get_request_user)):
    notebook = await service.create(user.id)

    return success_response(data=NotebookPublic.model_validate(notebook), status_code=HTTP_201_CREATED)


@router.put('/{uid}')
async def update(uid: UUID, service: NotebookServiceDep, request: NotebookUpdateRequest,
                 user=Depends(get_request_user)):
    notebook = await service.update_notebook(uid, user.id, request)

    return success_response(data=NotebookPublic.model_validate(notebook), status_code=HTTP_200_OK)


@router.delete('/{uid}')
async def destroy(uid: UUID, service: NotebookServiceDep, user=Depends(get_request_user)):
    await service.delete_notebook(uid, user.id)

    return success_response(status_code=status.HTTP_204_NO_CONTENT)
