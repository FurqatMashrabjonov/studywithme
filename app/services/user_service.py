from .base_service import BaseService
from app.dependencies.repository_dependency import UserRepositoryDep


class UserService(BaseService):
    def __init__(self, repository: UserRepositoryDep):
        self.repository = repository