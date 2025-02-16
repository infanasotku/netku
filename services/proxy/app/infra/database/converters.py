from app.schemas.proxy import ProxyInfoCreateSchema, ProxyInfoSchema
from app.infra.database.models import ProxyInfo


def proxy_create_schema_to_proxy_infp(proxy_create: ProxyInfoCreateSchema) -> ProxyInfo:
    return ProxyInfo(uuid=proxy_create.uuid, last_update=proxy_create.last_update)


def proxy_to_proxy_info_schema(proxy_info: ProxyInfo) -> ProxyInfoSchema:
    return ProxyInfoSchema.model_validate(proxy_info)
