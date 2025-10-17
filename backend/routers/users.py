from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas
import crud
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(crud.get_current_active_user)):
    return current_user