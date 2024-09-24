import logging

from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session

from .crud import get_user_projects_list, get_user_project, create_user_project, update_user_project, delete_user_project
from .schemas import CreateProjectSchema, ProjectSchema, UpdateProjectSchema

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


@project_router.post("/", response_model=ProjectSchema)
def new_project(new_project: CreateProjectSchema, user: User = Depends(check_current_user_active), db: Session = Depends(get_db)):
    logger.info("Creating new project")
    logger.debug(f"New Project: {new_project}")
    project_response = create_user_project(
        db = db, 
        user_id = user.id, 
        new_project = new_project
    )

    return project_response


@project_router.get("/{project_id}", response_model=ProjectSchema)
def get_project(project_id, user: User = Depends(check_current_user_active), db: Session = Depends(get_db)):
    user_project = get_user_project(
        db = db, 
        project_id = project_id
    )
    if user_project.user_id == user.id: 
        return user_project
    else: 
        raise  HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to view this project"
        )


@project_router.post("/{project_id}", response_model=ProjectSchema)
def update_project(project_id, updated_project: UpdateProjectSchema, user: User = Depends(check_current_user_active), db: Session = Depends(get_db)):
    __current_project = get_user_project(db=db, project_id=project_id)
    if __current_project.user_id == user.id: 
       updated_project = update_user_project(db=db, user_id=user.id, project_id=project_id, updated_project=updated_project)
       return updated_project
    else: 
        raise  HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to edit this project"
        )

@project_router.delete("/{project_id}")
def delete_project(project_id: int, user: User = Depends(check_current_user_active), db: Session = Depends(get_db)):
    try: 
        delete_user_project(db=db, project_id=project_id, user_id=user.id)
        return True
    except Exception as err:
        logger.error(f"Exception: {err}")
        raise  HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to delete this project"
        )