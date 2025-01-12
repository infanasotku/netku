from common.config import (
    PostgreSQLSettings,
    NetworkSettings,
    AuthSettings,
    AdminSettings,
)


class Settings(PostgreSQLSettings, NetworkSettings, AuthSettings, AdminSettings):
    pass
