from datetime import datetime

from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext


def get_password_hash(password: str):
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    return pwd_context.encrypt(password)


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.CreateUser):
    print("Creating User")
    hash_password = get_password_hash(user.password)
    print(hash_password)
    db_user = models.User(
        email=user.email,
        hashed_password=hash_password,
        full_name=user.full_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(db_user)
    return {'email': db_user.email, 'id': db_user.id}


def activate_user(db: Session, user_email: str, activation_code: str):
    user = db.query(models.User).filter(models.User.email == user_email).first()
    test_code = "signup123"
    if activation_code == test_code:
        user.is_active = True
        db.commit()
        db.refresh(user)
        if user.is_active:
            print(f"User Activated: {user}")
            return True
        else:
            print(f"User Not Activated: {user}")
            return False


def create_completedtask(db: Session,
                         completedtask: schemas.CreateCompletedTask,
                         user_id: int):
    db_task = models.CompletedTask(
        description=completedtask.description,
        user_id=user_id,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_completed_tasks(db: Session, user_id: int,
                        skip: int = 0, limit: int = 100):
    return (db.query(models.CompletedTask)
            .filter(models.CompletedTask.user_id == user_id)
            .offset(skip).limit(limit).all())


def get_completed_task_for_user_query(db: Session,
                                      user_id: int, skip: int = 0,
                                      limit: int = 100,
                                      from_date: datetime = None,
                                      to_date: datetime = None):
    query_filter = (db.query(models.CompletedTask)
                    .filter(models.CompletedTask.user_id == user_id))
    if from_date:
        print(f"From: {from_date}")
        query_filter = (query_filter
                        .filter(models.CompletedTask.created_at >= from_date))
    if to_date:
        print(f"To: {to_date}")
        query_filter = query_filter.filter(models.CompletedTask.created_at <= to_date)
    results = (query_filter
               .offset(skip).limit(limit).all())
    return results
