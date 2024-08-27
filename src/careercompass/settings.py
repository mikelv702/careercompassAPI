from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50

    db_user: str = "careercompass_user"
    db_password: str = "P@ssword"
    db_host: str = "dbhost"
    db_name: str = "careercompass"
    db_local: bool = False

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_app_settings():
    return Settings()
