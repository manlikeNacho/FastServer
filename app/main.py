from .db import engine
from . import models
from fastapi import FastAPI
from .utils import hash
from .routers import user, auth


app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=engine)


# Routes
app.include_router(user.router, prefix="/users", tags=['Users'])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])


@app.get("/")
async def root():
    return {"message": "Hello World From nacho!!"}
