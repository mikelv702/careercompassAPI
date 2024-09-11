import logging

from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session

from .crud import get_user_projects_list, get_user_project, create_user_project, update_user_project
from .schemas import CreateProjectSchema, ProjectSchema

from ..auth.helpers import check_current_user_active
from ..dependency import get_db
from ..user.schemas import User


logger = logging.getLogger(__name__)

project_router = APIRouter(tags=["Projects"], prefix="/projects")


@project_router.get("/", response_model=list[ProjectSchema])
def list_user_projects(user: User = Depends(check_current_user_active), db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    project_list = get_user_projects_list(
        db = db, 
        user_id = user.id, 
        skip = skip, 
        limit = limit
    )
    logger.info(f"Returning {len(project_list)} number of projects")
    return project_list


