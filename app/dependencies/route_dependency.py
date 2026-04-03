import uuid

from fastapi import Depends

from .service_dependency import NotebookServiceDep
from .security_dependency import get_request_user


async def get_valid_notebook(
    notebook_uid: uuid.UUID, service: NotebookServiceDep, user=Depends(get_request_user)
):
    notebook = await service.get_notebook_details(notebook_uid, user.id)

    return notebook
