from .. import models, schemas
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from ..database import get_db
from .. import models, utils, Oauth2
from sqlalchemy.orm import Session
from typing import List


user_router = APIRouter(
    prefix="/users",
    tags = ["Users"]
)

# Create a User
@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreate, db:Session = Depends(get_db)):
    user_email = db.query(models.User).filter(models.User.email == user.email).first()
    if user_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The User with email {user_email} already exists")
    new_password = utils.hash_passowrd(user.password)
    user.password = new_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return(new_user)


# Get all of the users
@user_router.get("/", status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db), 
                  curent_user: int = Depends(Oauth2.get_current_user)
                  ):
    print(curent_user.id)
    user = db.query(models.User).filter(models.User.id == curent_user.id).first()
    if user.is_admin:
        all_users = db.query(models.User).all()
        return all_users
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not authorized to perform this action"
    )
