import arrow
from pydantic import BaseModel, ConfigDict, computed_field, Field
from datetime import datetime


class BaseNote(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# DTOs
class NoteDto(BaseNote):
    title: str
    content: str


# Form Requests
class NoteUpdateRequest(BaseNote):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)


# Resources
class NoteListResource(BaseNote):
    title: str
    created_at: datetime

    @computed_field
    @property
    def created_at_formatted(self) -> str:
        return arrow.get(self.created_at).humanize(locale="uz")


class NoteResource(BaseNote):
    title: str
    content: str
