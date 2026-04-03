from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from app.models.user import User


class Notebook(Base):
    __tablename__ = "notebooks"

    uid: Mapped[uuid.UUID] = mapped_column(index=True, unique=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column("user_id", ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="notebooks")
