from typing import Optional, List
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException
from numpy import deprecate
from sqlalchemy.orm import Session
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import SessionLocal, engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}