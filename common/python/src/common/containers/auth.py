from dependency_injector import containers, providers

from common.auth.security import PyJWTSecurityClient
from common.containers.base import BaseContainer
from common.auth import RemoteAuthService


@containers.copy(BaseContainer)
class RemoteAuthContainer(BaseContainer):
    auth_service = providers.Singleton(
        RemoteAuthService,
        BaseContainer.config.auth_url,
        cliend_id=BaseContainer.config.client_id,
        client_secret=BaseContainer.config.client_secret,
        with_ssl=BaseContainer.config.with_auth_ssl,
    )


@containers.copy(BaseContainer)
class LocalAuthContainer(BaseContainer):
    security_client = providers.Singleton(
        PyJWTSecurityClient,
        BaseContainer.config.public_key,
        BaseContainer.config.private_key,
    )
