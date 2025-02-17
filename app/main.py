import os
from dotenv import load_dotenv
from .db import engine
from . import models
from fastapi import FastAPI
from .utils import hash
from .routers import user, auth


load_dotenv()

# Verify environment variables
print("DATABASE_URL:", os.getenv("DATABASE_URL"))
print("SECRET_KEY:", os.getenv("SECRET_KEY"))
print("ALGORITHM:", os.getenv("ALGORITHM"))
print("ACCESS_TOKEN_EXPIRE_MINUTES:", os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
print("EMAIL_RESET_TOKEN_EXPIRE_HOURS:",
      os.getenv("EMAIL_RESET_TOKEN_EXPIRE_HOURS"))

app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=engine)


# Routes
app.include_router(user.router, prefix="/users", tags=['Users'])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])


@app.get("/")
async def root():
    return {"message": "Hello World From nacho!!"}
