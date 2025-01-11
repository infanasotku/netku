from dependency_injector import containers, providers

from common.containers.base import BaseContainer
from common.auth.remote_auth import RemoteAuthService


@containers.copy(BaseContainer)
class AuthContainer(BaseContainer):
    auth_service = providers.Singleton(
        RemoteAuthService,
        BaseContainer.config.auth_url,
        cliend_id=BaseContainer.config.client_id,
        client_secret=BaseContainer.config.client_secret,
        with_ssl=BaseContainer.config.with_auth_ssl,
    )
