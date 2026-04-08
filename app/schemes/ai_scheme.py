import uuid

from pydantic import BaseModel


class AiRequest(BaseModel):
    message: str

class AiResponse(BaseModel):
    text: str
    total_token_usage: int

class StateDelta(BaseModel):
    notebook_id: int
