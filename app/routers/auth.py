import datetime
import traceback
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..schema import CreateUser, UserLogin, UserResp
from ..utils import verify_password, hash
from .. import models
from ..db import get_db
from ..oauth2 import create_access_token

router = APIRouter()


@router.post("/login")
def login(user_cred: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_cred.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # if not user.password != user_cred.password:
    #     raise HTTPException(status_code=401, detail="Invalid email/Password")

    access_token = create_access_token(data={"user_id": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResp)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    current_time = datetime.datetime.utcnow()
    try:

        # Ensure correct model dump for Pydantic
        new_user = models.User(**user.model_dump(), created_at=current_time)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserResp(id=str(new_user.id), email=new_user.email)

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

    except Exception as e:
        print(f"Exception: {str(e)} at {traceback.format_exc()}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
