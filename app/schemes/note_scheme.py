import arrow
from pydantic import BaseModel, ConfigDict, computed_field, Field
from datetime import datetime


class BaseNote(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# DTOs
class NoteDto(BaseNote):
    title: str
    content: str
    notebook_id: int


# Form Requests
class NoteCreateRequest(BaseNote):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class NoteUpdateRequest(BaseNote):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)


# Resources
class NoteListResource(BaseNote):
    id: int
    title: str
    type: str
    created_at: datetime

    @computed_field
    @property
    def created_at_formatted(self) -> str:
        return arrow.get(self.created_at).humanize(locale="uz")


class NoteResource(BaseNote):
    id: int
    title: str
    content: str
