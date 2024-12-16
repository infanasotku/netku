from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.infra.database.sql_db import get_db_factory as get_sql_db_factory
from app.infra.database.sql_db.orm import GetSQLDB
from app.infra.database.mongo_db import get_db_factory as get_mongo_db_factory
from app.infra.database.mongo_db.orm import GetMongoDB

from app.contracts.protocols import CreateRepository, CreateClient, CreateService

from app.contracts.repositories import (
    AvailabilityRepository,
    BookingRepository,
    UserRepository,
    XrayRepository,
)

from app.infra.database.sql_db.repositories import (
    SQLBookingRepository,
    SQLUserRepository,
    SQLXrayRepository,
    SQLRepositoryFactory,
)
from app.infra.database.mongo_db.repositories import (
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


from app.infra.config.settings import Settings


class AssistantDependencies:
    def __init__(self, settings: Settings):
        self._settings = settings
        self.bot: Bot = None
        self._create_bot()

        self.get_sql_db: GetSQLDB
        self.get_mongo_db: GetMongoDB
        self._init_databases()

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

    def _create_bot(self):
        self.bot = Bot(
            token=self._settings.bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

    def _init_databases(self):
        async_engine = create_async_engine(self._settings.psql_dsn)
        async_session = async_sessionmaker(async_engine)
        self.get_sql_db = get_sql_db_factory(async_session)

        self.get_mongo_db = get_mongo_db_factory(
            self._settings.mongo_dsn, self._settings.mongo_db_name
        )

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
