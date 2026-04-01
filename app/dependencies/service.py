from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.services.auth import AuthService
from app.services.user import UserService

DbSession = Annotated[AsyncSession, Depends(get_db)]

#Service dependencies
UserServiceDep = Annotated[UserService, Depends(UserService)]
AuthServiceDep = Annotated[AuthService, Depends(AuthService)]

#Repository dependencies
