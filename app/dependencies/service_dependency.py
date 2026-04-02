from typing import Annotated
from fastapi import Depends
from app.services.auth_service import AuthService
from app.services.notebook_service import NotebookService
from app.services.user_service import UserService

UserServiceDep = Annotated[UserService, Depends(UserService)]
AuthServiceDep = Annotated[AuthService, Depends(AuthService)]
NotebookServiceDep = Annotated[NotebookService, Depends(NotebookService)]
