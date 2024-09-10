import logging

from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session

from .crud import create_completedtask,get_completed_task_for_user_query
from .schemas import CompletedTaskBase, CreateCompletedTask

from ..auth import get_current_active_user
from ..dependency import get_db
from ..schemas import User


logger = logging.getLogger(__name__)

tasks_router = APIRouter(tags=["Tasks"])


@tasks_router.get('/task', response_model=list[CompletedTaskBase])
async def get_completed_tasks_for_user(user: User = Depends(get_current_active_user), db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    logger.debug(f"Getting tasks for user_id: {user.id}")
    if limit > 100: 
        logger.error('Requested limit of tasks is over 100!')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit for get /task exceeded"
        )
    current_user_tasks = get_completed_task_for_user_query(db=db, user_id=user.id, skip=skip, limit=limit)

    return current_user_tasks


@tasks_router.post("/task", response_model=CompletedTaskBase)
async def create_completed_task_for_user(task: CreateCompletedTask, user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    logger.debug(f"Creating task for user: {user.id}, task: {task}")
    completed_task = create_completedtask(db=db, completedtask=task, user_id=user.id)
    logger.info(f"Task Created: {completed_task}")
    return completed_task