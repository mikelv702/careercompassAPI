import jwt
from fastapi import Header, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param

from ..settings import get_app_settings


settings = get_app_settings()

def get_user_from_header(*, authorization: str = Header(None)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    scheme, token = get_authorization_scheme_param(authorization)
    if scheme.lower() != "bearer":
        raise credentials_exception

    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=['HS256']
        )
        # Retruning just the payload for now since we are not creating tokens with UserData
        return payload
    except jwt.PyJWTError:
        raise credentials_exception