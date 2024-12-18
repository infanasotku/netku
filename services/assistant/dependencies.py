from logging import Logger
from typing import Callable
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot
from pika import BlockingConnection

from app.infra.messaging.rabbitmq_connector import RabbitMQConnector
from app.infra.tasks.celery_connector import CeleryConnector

from app.infra.database.postgres_connection import PostgreSQLConnection
from app.adapters.output.database.sql_db.orm import GetSQLDB
from app.infra.database.mongo_connection import MongoDBConnection
from app.adapters.output.database.mongo_db.orm import GetMongoDB

from app.contracts.protocols import CreateRepository, CreateClient, CreateService

from app.contracts.repositories import (
    AvailabilityRepository,
    BookingRepository,
    UserRepository,
    XrayRepository,
)

from app.adapters.output.database.sql_db.repositories import (
    SQLBookingRepository,
    SQLUserRepository,
    SQLXrayRepository,
    SQLRepositoryFactory,
)
from app.adapters.output.database.mongo_db.repositories import (
    MongoAvailabilityRepository,
    MongoRepositoryFactory,
)

from app.contracts.clients import (
    AssistantClient,
    XrayClient,
    BookingClient,
    NotificationClient,
)
from app.adapters.output.grpc import (
    GRPCXrayClientFactory,
    GRPCBookingClientFactory,
)
from app.adapters.output.http import (
    HTTPAssistantClientFactory,
    AiogramNotificationClientFactory,
)

from app.contracts.services import (
    UserService,
    BookingAnalysisService,
    BookingService,
    XrayService,
    AvailabilityService,
)
from app.services import (
    UserServiceFactory,
    BookingServiceFactory,
    XrayServiceFactory,
    BookingAnalysisServiceFactory,
    AvailabilityServiceFactory,
)

from app.adapters.tasks.restart_proxy import RestartProxyTask


from app.infra.config.settings import Settings


class AssistantDependencies:
    def __init__(self, settings: Settings, logger: Logger):
        self._settings = settings
        self._logger = logger

        self.bot: Bot = None
        self._create_bot()

        self.get_sql_db: GetSQLDB
        self.get_mongo_db: GetMongoDB
        self._init_databases()

        self.get_rabbit_connection: Callable[[], BlockingConnection]
        self._init_message_broker()

        self.celery_connector: CeleryConnector
        self._init_celery_connector()

        self.create_xray_repo: CreateRepository[XrayRepository]
        self.create_user_repo: CreateRepository[UserRepository]
        self.create_booking_repo: CreateRepository[BookingRepository]
        self.create_availability_repo: CreateRepository[AvailabilityRepository]
        self._init_repositories()

        self.create_booking_client: CreateClient[BookingClient]
        self.create_xray_client: CreateClient[XrayClient]
        self.create_assistant_client: CreateClient[AssistantClient]
        self.create_notification_client: CreateClient[NotificationClient]
        self._init_clients()

        self.create_user_service: CreateService[UserService]
        self.create_booking_service: CreateService[BookingService]
        self.create_booking_analysis_service: CreateService[BookingAnalysisService]
        self.create_xray_service: CreateService[XrayService]
        self.create_availability_service: CreateService[AvailabilityService]
        self._init_services()

        self.restart_proxy: RestartProxyTask
        self._init_tasks()

    # External
    def _create_bot(self):
        self.bot = Bot(
            token=self._settings.bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

    def _init_databases(self):
        self.sql_connection = PostgreSQLConnection(self._settings.psql_dsn)
        self.get_sql_db = self.sql_connection.get_db

        self.mongo_connection = MongoDBConnection(
            self._settings.mongo_dsn, self._settings.mongo_db_name
        )
        self.get_mongo_db = self.mongo_connection.get_db

    def _init_message_broker(self):
        self.rabbitmq_connector = RabbitMQConnector(
            self._settings.rabbit_user,
            self._settings.rabbit_pass,
            self._settings.rabbit_host,
            self._settings.rabbit_port,
        )
        self.get_rabbit_connection = self.rabbitmq_connector.get_connection

    def _init_celery_connector(self):
        self.celery_connector = CeleryConnector(
            self._settings.rabbit_user,
            self._settings.rabbit_pass,
            self._settings.rabbit_host,
            self._settings.rabbit_port,
            "assistant_tasks",
        )

    # Internal
    def _init_repositories(self):
        self.create_xray_repo = SQLRepositoryFactory(
            self.get_sql_db, SQLXrayRepository
        ).create
        self.create_user_repo = SQLRepositoryFactory(
            self.get_sql_db, SQLUserRepository
        ).create
        self.create_booking_repo = SQLRepositoryFactory(
            self.get_sql_db, SQLBookingRepository
        ).create
        self.create_availability_repo = MongoRepositoryFactory(
            self.get_mongo_db, MongoAvailabilityRepository
        ).create

    def _init_clients(self):
        settings = self._settings

        self.create_booking_client = GRPCBookingClientFactory(
            client_addr=settings.booking_host,
            client_port=settings.booking_port,
            reconnection_delay=settings.reconnection_delay,
        ).create
        self.create_xray_client = GRPCXrayClientFactory(
            client_addr=settings.xray_host,
            client_port=settings.xray_port,
            reconnection_delay=settings.reconnection_delay,
        ).create
        self.create_assistant_client = HTTPAssistantClientFactory(
            assistant_addr=""
        ).create
        self.create_notification_client = AiogramNotificationClientFactory(
            bot=self.bot
        ).create

    def _init_services(self):
        self.create_user_service = UserServiceFactory(
            self.create_user_repo, self.create_notification_client
        ).create
        self.create_booking_service = BookingServiceFactory(
            self.create_booking_repo, self.create_booking_client
        ).create
        self.create_booking_analysis_service = BookingAnalysisServiceFactory(
            self.create_booking_service, self.create_user_service
        ).create
        self.create_xray_service = XrayServiceFactory(
            self.create_xray_repo, self.create_xray_client
        ).create
        self.create_availability_service = AvailabilityServiceFactory(
            self.create_booking_client,
            self.create_xray_client,
            self.create_assistant_client,
            self.create_availability_repo,
            self.create_user_service,
        ).create

    async def close_dependencies(self):
        await self.bot.session.close()

    def _init_tasks(self):
        self.restart_proxy = RestartProxyTask(
            self._logger,
            self.celery_connector.celery,
            self.bot,
            self.create_user_service,
            self.create_xray_service,
        )
