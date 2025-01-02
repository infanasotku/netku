from typing import Callable, AsyncContextManager, TypeVar

from common.contracts.repository import BaseRepository
from common.contracts.service import BaseService
from common.contracts.client import BaseClient


RepositoryT = TypeVar("RepositoryT", bound=BaseRepository)
ServiceT = TypeVar("ServiceT", bound=BaseService)
ClientT = TypeVar("ClientT", bound=BaseClient)

CreateRepository = Callable[[], AsyncContextManager[RepositoryT]]
CreateService = Callable[[], AsyncContextManager[ServiceT]]
CreateClient = Callable[[], AsyncContextManager[ClientT]]
