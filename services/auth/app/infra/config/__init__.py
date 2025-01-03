from common.config import PostgreSQLSettings, NetworkSettings, AdminSettings


class Settings(PostgreSQLSettings, NetworkSettings, AdminSettings):
    pass
