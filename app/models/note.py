from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class Note(Base):
    __tablename__ = "notes"

    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    notebook_id: Mapped[int] = mapped_column(ForeignKey("notebooks.id"))
    # notebook: Mapped["Notebook"] = relationship(back_populates="notebooks")
