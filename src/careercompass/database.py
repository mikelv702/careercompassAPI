from sqlalchemy import create_engine, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import get_app_settings

settings = get_app_settings()

if not settings.db_local:

    SQLALCHEMY_DATABASE_URL = URL.create(
        "postgresql",
        username=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        database=settings.db_name
    )
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./foo.db"
    # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
