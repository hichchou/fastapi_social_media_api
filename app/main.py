from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

#no longer needed, handled by alembic for generating tables
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# select domains allowed to access API
# origins = [
#     "http://localhost",
#     "http://localhost:8080",
#     "https://www.google.com"
# ]
#allow all domains (wild card)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Hello World !!"}