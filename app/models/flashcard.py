from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base


class Flashcard(Base):
    __tablename__ = "flashcards"

    title: Mapped[str] = mapped_column(String, nullable=False)
    notebook_id: Mapped[int] = mapped_column(ForeignKey("notebooks.id"))



    items=relationship("FlashcardItem", back_populates="flashcard", cascade="all, delete-orphan")