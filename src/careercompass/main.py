from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_active_user
from .crud import activate_user, create_completedtask, create_user, get_completed_task_for_user_query, get_user_by_email
from .dependency import get_db
from .schemas import CompletedTask, CreateCompletedTask, CreateUser, Token, User
from .settings import get_app_settings

settings = get_app_settings()
app = FastAPI()

print(settings.allowed_origins)
app.add_middleware(CORSMiddleware, 
                allow_origins=settings.allowed_origins, 
                allow_credentials=True,
                allow_methods=["*"], 
                allow_headers=["*"])

@app.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)) -> Token:
    user = authenticate_user(db=db,
                             username=form_data.username,
                             password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.post("/user")
async def register_new_user(user: CreateUser, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return create_user(db=db, user=user)


@app.post("/user/activate/")
async def activate_registered_user(email: str,
                                   activation_code: str,
                                   db: Session = Depends(get_db)):
    if activate_user(db=db, user_email=email, activation_code=activation_code):
        return {"status": "success"}
    else:
        return {"status": "failed"}


@app.get("/user/me", response_model=User)
async def get_logged_in_user(logged_in_user: User = Depends(get_current_active_user)):
    return logged_in_user


@app.get("/task", response_model=list[CompletedTask])
async def get_user_completed_tasks(user: User = Depends(get_current_active_user),
                                   db: Session = Depends(get_db),
                                   skip: int = 0, limit: int = 10):
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can not get more than 100 tasks",
        )
    tasks = get_completed_task_for_user_query(db=db,
                                              user_id=user.id,
                                              skip=skip,
                                              limit=limit)
    print(f"Number of tasks: {len(tasks)}")
    return tasks


@app.post("/task", response_model=CompletedTask)
async def create_user_completed_task(task: CreateCompletedTask,
                                     user: User = Depends(get_current_active_user),
                                     db: Session = Depends(get_db)):
    completed_task = create_completedtask(db=db, completedtask=task, user_id=user.id)
    print(completed_task)
    return completed_task


# Health Check
@app.get('/health')
async def health_check():
    return {"status": "ok"}