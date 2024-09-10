from datetime import datetime
import logging

from sqlalchemy.orm import Session

from .schemas import CreateCompletedTask
from .models import CompletedTask


logger = logging.getLogger(__name__)

def create_completedtask(db: Session, completedtask: CreateCompletedTask, user_id: int):
    logger.info(f"Creating task for {user_id}")
    db_task = CompletedTask(
        description=completedtask.description, 
        user_id=user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_completed_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    db_results = db.query(CompletedTask).filter(CompletedTask.user_id == user_id).offset(skip).limit(limit).all()
    logger.info(f"Number of results found: {len(db_results)}")
    return db_results


def get_completed_task_for_user_query(db: Session, user_id: int, skip: int = 0, limit: int = 100, from_date: datetime = None, to_date: datetime = None):
    try:
        db_query = db.query(CompletedTask)
        db_query_filter = [CompletedTask.user_id == user_id]

        if from_date: 
            logger.info(f"Query Tasks created after: {from_date}")
            db_query_filter.append(CompletedTask.created_at >= from_date)
        
        if to_date: 
            logger.info(f"Query Tasks created before: {to_date}")
            db_query_filter.append(CompletedTask.created_date <= to_date)

        db_results = db_query.filter(*db_query_filter).offset(skip).limit(limit).all()
        logger.info(f"Number of results found: {len(db_results)}")
        return db_results
    except Exception as e: 
        logger.error(f"Unhandled Exception: {e}")