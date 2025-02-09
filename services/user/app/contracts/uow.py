from common.contracts.uow import BaseUnitOfWork

from app.contracts.repositories import UserRepository


class UserUnitOfWork(BaseUnitOfWork):
    user: UserRepository
