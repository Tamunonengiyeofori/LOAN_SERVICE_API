from .. import models, schemas
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter, Response
from ..database import get_db, engine
from .. import models, utils, Oauth2
from sqlalchemy.orm import Session
from typing import List
from faker import Faker



user_router = APIRouter(
    prefix="/users",
    tags = ["Users"]
)

fake = Faker()

ADMIN_USER = ""

# Create an Admin at startup
@user_router.on_event("startup")
async def create_startup_admin():
    global ADMIN_USER
    admin_email = fake.email()
    admin_password = "123456"
    with Session(engine) as session:
        user = session.query(models.User).filter(models.User.email == admin_email).first()
        if user is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"User with email: {admin_email} already exists")
        admin_password = utils.hash_passowrd(admin_password)
        new_user = models.User(email=admin_email,
                            password=admin_password,
                            is_admin=True)
        session.add(new_user)
        ADMIN_USER = new_user.email
        session.commit()
        session.refresh(new_user)
        
#Delete admin at server shutdown
@user_router.on_event("shutdown")
async def delete_admins():
    global ADMIN_USER
    with Session(engine) as session:
        admin_user = session.query(models.User).filter(models.User.email == ADMIN_USER).first()
        if admin_user:
            session.delete(admin_user)
            session.commit()
  


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
    return Response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content="You are not authorized to perform this action"
    )
