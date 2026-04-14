from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.repositories.flashcard_repository import FlashcardRepository
from app.repositories.notebook_repository import NotebookRepository
from app.repositories.user_repository import UserRepository
from app.repositories.note_repository import NoteRepository

DbSession = Annotated[AsyncSession, Depends(get_db)]

UserRepositoryDep = Annotated[UserRepository, Depends(UserRepository)]
NotebookRepositoryDep = Annotated[NotebookRepository, Depends(NotebookRepository)]
NoteRepositoryDep = Annotated[NoteRepository, Depends(NoteRepository)]
FlashcardRepositoryDep = Annotated[FlashcardRepository, Depends(FlashcardRepository)]