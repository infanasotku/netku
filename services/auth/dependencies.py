from logging import Logger

from common.sql.orm import GetSQLDB
from common.sql.postgres_connection import PostgreSQLConnection

from app.infra.config import Settings


class AuthDependencies:
    def __init__(self, settings: Settings, logger: Logger):
        self._settings = settings
        self._logger = logger

        self.get_sql_db: GetSQLDB
        self._init_databases()

        self._init_repositories()

        self._init_services()

    def _init_databases(self):
        self.sql_connection = PostgreSQLConnection(
            self._settings.psql_dsn, self._settings.psql_schema
        )
        self.get_sql_db = self.sql_connection.get_db

    def _init_repositories(self):
        pass

    def _init_services(self):
        pass
