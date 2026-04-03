from fastapi import FastAPI
from fastapi import Depends

from app.core.exceptions import AppException
from app.dependencies.security_dependency import get_request_user
from routes.auth import router as auth_router
from routes.notebook import router as notebook_router
from routes.note import router as note_router
from app.core.exception_handlers import app_exception_handler

app = FastAPI()

app.add_exception_handler(AppException, app_exception_handler)

app.include_router(prefix="/auth", router=auth_router, tags=["Auth"])

app.include_router(
    prefix="/notebook",
    router=notebook_router,
    tags=["Notebook"],
    dependencies=[Depends(get_request_user)],
)

app.include_router(
    prefix="/{notebook_uid}/note",
    router=note_router,
    tags=["Note"],
    dependencies=[Depends(get_request_user)],
)
