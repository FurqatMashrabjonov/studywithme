import uuid

from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base



class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column('name', String, nullable=False)
    email: Mapped[str] = mapped_column('email', String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column('password', String, nullable=False)