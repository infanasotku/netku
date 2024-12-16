from typing import Callable, AsyncContextManager, TypeVar

from app.contracts.repositories.base import BaseRepository
from app.contracts.clients.base import BaseClient
from app.contracts.services.base import BaseService


RepositoryT = TypeVar("RepositoryT", bound=BaseRepository)
ClientT = TypeVar("ClientT", bound=BaseClient)
ServiceT = TypeVar("ServiceT", bound=BaseService)

CreateRepository = Callable[[], AsyncContextManager[RepositoryT]]
CreateClient = Callable[[], AsyncContextManager[ClientT]]
CreateService = Callable[[], AsyncContextManager[ServiceT]]
