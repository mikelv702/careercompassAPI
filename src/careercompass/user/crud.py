import logging
from sqlalchemy.orm import Session

from .models import User
from .schemas import CreateUser

from ..settings import get_app_settings
from ..auth.hash import get_password_hash

settings = get_app_settings()
logger = logging.getLogger(__name__)


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: CreateUser):
    logger.info(f"Creating new user: {user.email}, {user.full_name}")
    hashed_password = get_password_hash(user.password)
    logger.debug(f"Hashed Password: {hashed_password}")
    user_model = User(
        email=user.email, 
        hashed_password=hashed_password, 
        full_name=user.full_name
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    logger.info(f"User created: {user_model.id}")
    return {'email': user_model.email, 'id': user_model.id} # Convert to Pydantic Model?


def activate_user(db: Session, user_email: str, activation_code: str):
    user = db.query(User).filter(User.email == user_email).first()
    if activation_code == settings.signup_key:
        user.is_active = True
        db.commit()
        db.refresh(user)
    if user.is_active:
        logger.info(f"Activated User: {user}")
        return True
    else: 
        logger.info(f"Unable to activate user: {user}")
        return False