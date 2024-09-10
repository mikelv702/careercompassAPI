import bcrypt
import jwt
import logging
from datetime import datetime, timedelta
from typing import Annotated
from jwt.exceptions import InvalidTokenError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from .schemas import TokenData

from ..settings import get_app_settings
from ..dependency import get_db
from ..user.schemas import User
from ..user.crud import get_user_by_email


logger = logging.getLogger(__name__)
settings = get_app_settings()

SECRET_KEY = settings.secret_key
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


CREDENTIAL_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

USER_UNAUTHORIZED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User is not authorized.",
)


def verify_user_password(plain_password: str, hash_password: str) -> bool:
    result = bcrypt.checkpw(plain_password.encode('utf-8'), hash_password.encode('utf-8'))
    if result is False: 
        logger.error('Unable to verify password')
    return result


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    data_to_encode = data.copy()
    if expires_delta:
        token_expire = datetime.now() + expires_delta
    else:
        logger.info(f"Token Expiry not supplied defaulting to {ACCESS_TOKEN_EXPIRE_MINUTES}.")
        token_expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({'exp': token_expire})
    logger.debug(f"Data to encode:{data_to_encode}")
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.debug(f"Access Token issued: {encoded_jwt}")
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    logger.debug(f"token: {token}")
    try:
        token_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"Token Payload: {token_payload}")
        email = token_payload.get("sub")
        if email is None:
            raise CREDENTIAL_EXCEPTION
        token_data = TokenData(email=email)
        logger.debug(f"Token Data: {token_data}")
        return token_data
    except InvalidTokenError as e:
        logger.error(f"Invalid Token Error: {token}; Error: {e}")
        raise CREDENTIAL_EXCEPTION
    except DecodeError as e:
        logger.error(f"Decode Error: {token}; Error: {e}")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    logger.info('Decoding Token')
    token_data = decode_access_token(token)
    current_user = get_user_by_email(db, email=token_data.email)
    if current_user is None:
        logger.error(f'Current User is None')
        raise CREDENTIAL_EXCEPTION
    logger.info('Current User Found')
    logger.debug(f"Current User: {current_user}")
    return current_user


def check_current_user_active(current_user: Annotated[User, Depends(get_current_user)]):
    logger.debug(f"Checking if user is active: {current_user}")
    if not current_user.is_active:
        logger.warn(f"User is not active: {current_user.id}")
        raise USER_UNAUTHORIZED_EXCEPTION
    return current_user


def authenticate_username_password(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=username)
    if not user.is_active:
        return False
    if not user: 
        return False
    if not verify_user_password(password, user.hashed_password):
        return False
    return user

    
