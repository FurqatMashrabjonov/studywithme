from typing import Annotated
from fastapi import Depends
from app.services.auth_service import AuthService
from app.services.flashcard_service import FlashcardService
from app.services.notebook_service import NotebookService
from app.services.note_service import NoteService
from app.services.user_service import UserService

UserServiceDep = Annotated[UserService, Depends(UserService)]
AuthServiceDep = Annotated[AuthService, Depends(AuthService)]
NotebookServiceDep = Annotated[NotebookService, Depends(NotebookService)]
NoteServiceDep = Annotated[NoteService, Depends(NoteService)]
FlashcardServiceDep = Annotated[FlashcardService, Depends(FlashcardService)]