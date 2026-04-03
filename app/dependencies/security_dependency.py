from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status
from app.core.exceptions import AppException
from app.dependencies.repository_dependency import UserRepositoryDep
from app.core.security import decode_token

security = HTTPBearer()


async def get_request_user(
    repository: UserRepositoryDep,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    if not credentials:
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED, message="User unauthorized"
        )

    token = credentials.credentials

    payload = decode_token(token)

    if payload is None:
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED, message="Token is not valid"
        )

    user_id = int(payload.get("user_id", 0))

    if user_id is None:
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED, message="Token is not valid"
        )

    user = await repository.get_user_by_id(user_id)

    if user is None:
        raise AppException(
            status_code=status.HTTP_404_NOT_FOUND, message="User not found"
        )

    return user
