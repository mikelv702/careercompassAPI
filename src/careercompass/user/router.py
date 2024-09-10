import logging

from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session

from .schemas import CreateUser, User
from .crud import get_user_by_email, create_user, activate_user

from ..dependency import get_db
from ..auth.helpers import check_current_user_active

logger = logging.getLogger(__name__)

user_router = APIRouter(prefix="/user",tags=["User"])

UNABLE_TO_REGISTER_USER = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Unable to register User"
)


@user_router.post('/')
async def register_new_local_user(user: CreateUser, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        logger.warn(f"User already registered: {user.email}")
        raise UNABLE_TO_REGISTER_USER
    try:
        db_user = create_user(db=db, user=user)
    except Exception as e: 
        logger.error(f"Failed to create user: {user}")
        logger.error(f"Failed to create user Exception: {e}")
        raise UNABLE_TO_REGISTER_USER
    
    return db_user


@user_router.post('/activate')
async def activate_registered_user(email: str, activation_code: str, db: Session = Depends(get_db)):
    activation_response = activate_user(db=db, user_email=email, activation_code= activation_code)
    if activation_response:
        return {"status": "success"}
    else:
        raise UNABLE_TO_REGISTER_USER


@user_router.get("/me", response_model=User)
async def get_current_user_profile(logged_in_user: User = Depends(check_current_user_active)):
    return logged_in_user