from common.config import PostgreSQLSettings, NetworkSettings, AuthSettings


class Settings(PostgreSQLSettings, NetworkSettings, AuthSettings):
    pass
