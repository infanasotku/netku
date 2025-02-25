from common.contracts.uow import BaseUnitOfWork

from app.contracts.repositories import ProxyInfoRepository


class ProxyUnitOfWork(BaseUnitOfWork):
    proxy: ProxyInfoRepository
