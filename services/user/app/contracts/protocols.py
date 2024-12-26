from typing import Callable, AsyncContextManager, TypeVar

from app.contracts.repositories.base import BaseRepository
from app.contracts.services.base import BaseService


RepositoryT = TypeVar("RepositoryT", bound=BaseRepository)
ServiceT = TypeVar("ServiceT", bound=BaseService)

CreateRepository = Callable[[], AsyncContextManager[RepositoryT]]
CreateService = Callable[[], AsyncContextManager[ServiceT]]
