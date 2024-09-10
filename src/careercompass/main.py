from datetime import timedelta
from typing import Annotated
import logging

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .auth.helpers import create_access_token, authenticate_username_password
from .dependency import get_db
from .schemas import Token
from .settings import get_app_settings

from .auth.router import auth_router
from .tasks.router import tasks_router
from .user.router import user_router


logger = logging.getLogger(__name__)


settings = get_app_settings()
if settings.app_log_debug:
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logger.debug('DEBUG ENABLED')
else:
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logger.info(f"DEBUG Logs: {settings.app_log_debug}")
    logger.info('DEBUG DISABLED')

logger.info('Settings Loaded...')
logger.debug(f"Settings Loaded: {settings}")


app = FastAPI()
logger.info("Loading Routers...")
app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(user_router)


logger.debug(f"Allowed Origins: {settings.allowed_origins}")
app.add_middleware(CORSMiddleware, 
                allow_origins=settings.allowed_origins, 
                allow_credentials=True,
                allow_methods=["*"], 
                allow_headers=["*"])


@app.post('/token')
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)) -> Token:
    user = authenticate_username_password(db=db,
                             username=form_data.username,
                             password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.debug(f"User: {user}")
    access_token_expires = timedelta(minutes=45)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


# @app.post('/user')
# async def register_new_user(user: CreateUser, db: Session = Depends(get_db)):
#     db_user = get_user_by_email(db, user.email)
#     if db_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email already registered",
#         )
#     return create_user(db=db, user=user)


# @app.post('/user/activate/')
# async def activate_registered_user(email: str,
#                                    activation_code: str,
#                                    db: Session = Depends(get_db)):
#     if activate_user(db=db, user_email=email, activation_code=activation_code):
#         return {"status": "success"}
#     else:
#         return {"status": "failed"}


# @app.get("/user/me", response_model=User)
# async def get_logged_in_user(logged_in_user: User = Depends(get_current_active_user)):
#     return logged_in_user



# Health Check
@app.get('/health')
async def health_check():
    logger.info('Health Check called...')
    return {"status": "ok"}