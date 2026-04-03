from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.notebook import Notebook


class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column("name", String, nullable=False)
    email: Mapped[str] = mapped_column("email", String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column("password", String, nullable=False)
    notebooks: Mapped[list["Notebook"]] = relationship(back_populates="user")
