from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base


class FlashcardItem(Base):
    __tablename__ = "flashcard_items"

    flashcard_id: Mapped[int] = mapped_column(ForeignKey("flashcards.id"))
    question: Mapped[str] = mapped_column(String, nullable=False)
    answer: Mapped[str] = mapped_column(String, nullable=False)

    flashcard = relationship("Flashcard", back_populates="items")