from urllib import response
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
import sqlalchemy
import Oauth2
import utils
import schemas, database, models
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session

auth_router = APIRouter(
    tags=["Authentication"]
)

@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
        
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
        
    #Create access token
    access_token = Oauth2.create_access_token(data = {"user_id" : user.id})
    return {"access_token" : access_token, 
            "token_type" : "bearer"}
