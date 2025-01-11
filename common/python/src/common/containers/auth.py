from dependency_injector import containers, providers

from common.containers.base import BaseContainer
from common.auth.remote_auth import RemoteAuthService


@containers.copy(BaseContainer)
class AuthContainer(BaseContainer):
    config = BaseContainer.config

    auth_service = providers.Singleton(
        RemoteAuthService,
        config.auth_url,
        cliend_id=config.client_id,
        client_secret=config.client_secret,
        with_ssl=config.with_ssl,
    )
