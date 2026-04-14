from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime

class BaseFlashcard(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# DTOs
class FlashcardItemDto(BaseFlashcard):
    question: str
    answer: str

class FlashcardDto(BaseFlashcard):
    title: str
    notebook_id: int
    cards: List[FlashcardItemDto]

# Resources
class FlashcardListResource(BaseFlashcard):
    id: int
    title: str
    created_at: datetime

class FlashcardItemResource(BaseFlashcard):
    id: int
    question: str
    answer: str

class FlashcardResource(BaseFlashcard):
    id: int
    title: str
    cards: List[FlashcardItemResource]