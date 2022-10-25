from typing import Optional, List
from fastapi import Body, Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    posts = db.query(models.Post).all()
    return posts

@router.get("/{id}", response_model=schemas.Post)
def get_post(
    id: int, 
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)
):
    # new_post = models.Post(
    #     title=post.title, content=post.content, published= post.published)
    #we can unpack dict automatically, more convenient that way
    print(current_user.email)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id={id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int, post: schemas.PostCreate, 
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id={id} does not exist")

    post_query.update(post.dict(),synchronize_session=False)
    db.commit()

    return post_query.first()