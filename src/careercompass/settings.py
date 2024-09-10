from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    app_log_debug: bool = False
    admin_email: str
    items_per_user: int = 50

    db_user: str = "careercompass_user"
    db_password: str = "P@ssword"
    db_host: str = "dbhost"
    db_name: str = "careercompass"
    db_local: bool = False
    
    allowed_origins: list[str] = ["http://localhost:3000"]
    secret_key: str = None
    signup_key: str = "signup123"
    github_client_id: str = None
    github_client_secret: str = None
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_app_settings():
    return Settings()
