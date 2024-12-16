from pydantic_settings import BaseSettings
from pydantic import Field, computed_field


class MongoSettings(BaseSettings):
    mongo_pass: str = Field(validation_alias="MONGO_PASSWORD")
    mongo_user: str = Field(validation_alias="MONGO_USER")
    mongo_host: str = Field(validation_alias="MONGO_HOST", default="127.0.0.1")
    mongo_port: int = Field(validation_alias="MONGO_PORT", default=27017)
    mongo_db_name: str = Field(validation_alias="MONGO_DB_NAME", default="mongo")

    @computed_field
    @property
    def mongo_dsn(self) -> str:
        return (
            f"mongodb://{self.mongo_user}:{self.mongo_pass}"
            + f"@{self.mongo_host}:{self.mongo_port}/"
        )
