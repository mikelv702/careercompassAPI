import logging

from sqlalchemy.orm import Session
from sqlalchemy import exc

from .models import ProjectsModel
from .schemas import CreateProjectSchema


logger = logging.getLogger(__name__)


def get_user_projects_list(db: Session, user_id: int, skip: int =0, limit: int = 100, **kwargs):
    try: 
        db_query = db.query(ProjectsModel)
        db_query_filter = [ProjectsModel.user_id == user_id]

        for key in kwargs.keys():
            logger.info(f"Query Key: {key}")
            
        
        query_result = db_query.filter(*db_query_filter).offset(skip).limit(limit).all()
        return query_result
    except exc.SQLAlchemyError:
        logger.error("SQL ERROR")
    except Exception as e: 
        logger.error(f"Unhandled Exception: {e}")


def get_user_project(db: Session, project_id: int):
    try: 
        db_query = db.query(ProjectsModel).filter(ProjectsModel.id == project_id).first()
        return db_query
    except exc.SQLAlchemyError:
        logger.error("SQL ERROR")
    except Exception as e: 
        logger.error(f"Unhandled Exception: {e}")


def create_user_project(db: Session, user_id: int, new_project: CreateProjectSchema):
    logger.info('Creating new project')
    try: 
        logger.info(f"User requested new project: {user_id}")
        logger.info(f"New Project: {new_project}")
        db_project = ProjectsModel(user_id = user_id, **new_project.model_dump())
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    except exc.SQLAlchemyError:
        logger.error("SQL ERROR")
    except Exception as e: 
        logger.error(f"Unhandled Exception: {e}")


def update_user_project(db: Session, user_id: int, project_id: int, updated_project: CreateProjectSchema):
    logger.info(f"Updating Project {project_id}")
    try: 
        current_db_project = db.query(ProjectsModel).filter(ProjectsModel.id == project_id).first()
        updated_project_dict = updated_project.model_dump(exclude_unset=True)
        logger.info(f"Settings to update: {updated_project_dict}")
        logger.info(f"Current DB object: {current_db_project}")
        for key, value in updated_project_dict.items():
            logger.info(f"Key: {key}, Value: {value}")
            setattr(current_db_project, key, value)
        logger.info(f"After update: {current_db_project}")
        db.commit()
        db.refresh(current_db_project)
        return current_db_project
    except exc.SQLAlchemyError:
        logger.error("SQL ERROR")
    except Exception as e: 
        logger.error(f"Unhandled Exception: {e}")    
