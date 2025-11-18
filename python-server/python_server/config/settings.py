from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_uri: SecretStr | None = None

    model_config = SettingsConfigDict(env_file=".env")

    @field_validator("db_uri")
    @classmethod
    def _check_db_uri(cls, db_uri_value: SecretStr | None) -> SecretStr:
        if db_uri_value is None:
            raise ValueError("DB_URI is missing from environment variables")
        return db_uri_value

    @property
    def db_uri_unwrapped(self) -> str:
        if self.db_uri is None:
            raise ValueError("DB_URI is missing from environment variables")
        return self.db_uri.get_secret_value()


settings = Settings()
