from common.events.proxy import ProxyInfoChangedEvent

from app.contracts.clients import ProxyClientPull, ProxyCachingClient
from app.contracts.services import ProxyService
from app.contracts.uow import ProxyUnitOfWork
from app.schemas.proxy import ProxyInfoCreateSchema, ProxyInfoUpdateSchema


class ProxyServiceImpl(ProxyService):
    def __init__(
        self,
        proxy_uow: ProxyUnitOfWork,
        proxy_clients_pull: ProxyClientPull,
        proxy_caching_client: ProxyCachingClient,
        info_event: ProxyInfoChangedEvent,
    ):
        self._proxy_uow = proxy_uow
        self._pull = proxy_clients_pull
        self._caching = proxy_caching_client
        self._info_event = info_event

    async def get_by_id(self, id):
        async with self._proxy_uow as uow:
            return await uow.proxy.get_by_id(id)

    async def restart_engine(self, id, uuid):
        async with self._proxy_uow as uow:
            info = await uow.proxy.get_by_id(id)

            if info is None:
                raise KeyError("Proxy info not exists.")

            client = self._pull.get(info.key)
            if client is None:
                raise KeyError(f"Proxy client for {id} not exists.")

            xray_uuid = await client.restart(uuid)
            if xray_uuid != uuid:
                raise RuntimeError("Xray uuid is different from the one transmitted.")

    async def pull(self):
        records = await self._caching.get_all()

        async with self._proxy_uow as uow:
            await uow.proxy.delete_all()

            for record in records:
                await uow.proxy.create(ProxyInfoCreateSchema.model_validate(record))

        return records

    async def pull_by_key(self, key):
        info = await self._caching.get_by_key(key)
        if info is None:
            raise KeyError("Proxy info not exists in cache.")

        async with self._proxy_uow as uow:
            old_info = await uow.proxy.get_by_key(key)
            if old_info is None:
                info_create = ProxyInfoCreateSchema.model_validate(info)
                info = await uow.proxy.create(info_create)
            else:
                info_update = ProxyInfoUpdateSchema(
                    running=info.running, uuid=info.uuid
                )
                info = await uow.proxy.update(old_info.id, info_update)

            await self._info_event.dispatch(info)
