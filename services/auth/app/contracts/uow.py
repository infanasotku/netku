from common.contracts.uow import BaseUnitOfWork

from app.contracts.repositories import ClientRepository, ClientScopeRepository


class ClientScopeUnitOfWork(BaseUnitOfWork):
    client: ClientRepository
    client_scope: ClientScopeRepository
