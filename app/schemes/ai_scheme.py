from pydantic import BaseModel, ConfigDict
from app.services.flashcard_service import FlashcardService

class AiRequest(BaseModel):
    message: str

class AiResponse(BaseModel):
    text: str
    total_token_usage: int

class StateDelta(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    notebook_id: int

class AiStreamResponse(BaseModel):
    type: str
    text: str
    finished: bool
