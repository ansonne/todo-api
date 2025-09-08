from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models, schemas, utils, database

router = APIRouter(prefix="/users", tags=["users"])
get_db = database.get_db


@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.scalar(
        select(models.User).filter(models.User.username == user.username)
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = utils.get_password_hash(user.password)
    new_user = models.User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.scalar(
        select(models.User).filter(models.User.username == user.username)
    )
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not utils.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = utils.create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}
