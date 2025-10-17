from sqlalchemy.orm import Session
import models
import schemas
from auth import get_password_hash

# 用户相关CRUD操作
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 文件相关CRUD操作
def get_files(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.File).filter(models.File.owner_id == user_id).offset(skip).limit(limit).all()

def get_file(db: Session, file_id: int, user_id: int):
    return db.query(models.File).filter(models.File.id == file_id, models.File.owner_id == user_id).first()

def create_file(db: Session, file: schemas.FileCreate, user_id: int):
    db_file = models.File(**file.dict(), owner_id=user_id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def delete_file(db: Session, file_id: int, user_id: int):
    db_file = get_file(db, file_id, user_id)
    if db_file:
        db.delete(db_file)
        db.commit()
        return True
    return False