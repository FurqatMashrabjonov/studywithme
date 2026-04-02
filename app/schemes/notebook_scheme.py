import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class BaseNotebook(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class NotebookDto(BaseNotebook):
    name: str
    user_id: int
    uid: uuid.UUID

class NotebookPublic(BaseNotebook):
    uid: uuid.UUID
    name: str
    created_at: datetime

class NotebookUpdateRequest(BaseNotebook):
    name: str

class NotebookUpdateDto(BaseNotebook):
    name: Optional[str] = None