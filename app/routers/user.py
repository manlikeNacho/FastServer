import datetime
from uuid import UUID
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..schema import User, UserResp, CreateUser
from ..utils import hash
from .. import models
from ..db import get_db

router = APIRouter()


@router.get("/{id}", response_model=UserResp)
def get_user(id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve a user by their ID.
    """
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id {id} not found")
    return user


@router.delete("/{id}")
def delete_user(id: UUID, db: Session = Depends(get_db)):
    """
    Delete a user by their ID.
    """
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id {id} not found")
    db.delete(user)
    db.commit()
    return {"message": f"User with id {id} was deleted"}


@router.put("/{id}", response_model=UserResp)
def updated_user(id: UUID, user: User, db: Session = Depends(get_db)):
    """
    Update a user by their ID.
    """
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(
            status_code=404, detail=f"User with id {id} not found")

    # Update user fields
    db_user.email = user.email
    db_user.name = user.name
    db_user.updated_at = datetime.datetime.now()

    db.commit()
    db.refresh(db_user)
    return db_user
