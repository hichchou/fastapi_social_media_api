from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils

router = APIRouter(
    tags= ['Authentification']
)

@router.post('/login')
def login(user_credential: schemas.UserLogin, db : Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credential.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    #create token
    #return token
    return {"token": "exemple token"}