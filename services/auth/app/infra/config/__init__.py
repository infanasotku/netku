from common.config import (
    PostgreSQLSettings,
    NetworkSettings,
    AdminSettings,
    LocalAuthSettings,
)


class Settings(PostgreSQLSettings, NetworkSettings, AdminSettings, LocalAuthSettings):
    pass
