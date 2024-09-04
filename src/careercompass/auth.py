from datetime import datetime, timedelta
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from .crud import get_user_by_email
from .dependency import get_db
from .schemas import TokenData, User
from .settings import get_app_settings

settings = get_app_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'  # FAKE
SECRET_KEY = settings.secret_key
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    result = bcrypt.checkpw(plain_password.encode('utf-8'),
                        hashed_password.encode('utf-8'))
    print(result)
    return result

# This function was moved to Crud to prevent duplication and circular dependencies
# Not the best implementation, but should be fixed during refactoring
# def get_password_hash(password: str) -> str:
#     salt = bcrypt.gensalt()
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
#     string_password = hashed_password.decode('utf-8')
#     return string_password


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
        print(token_data)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user_by_email(db, email=token_data.email)
    print(user)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def authenticate_user(username: str, password: str,
                      db: Session = Depends(get_db)):

    user = get_user_by_email(db, email=username)
    if not user.is_active:
        return False
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

