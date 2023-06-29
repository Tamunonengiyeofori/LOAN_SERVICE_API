import models, schemas
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from database import get_db
import models, utils, schemas
from sqlalchemy.orm import Session
import Oauth2

profile_router = APIRouter(
    prefix="/users/profile",
    tags = ["UserProfile"])

@profile_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user_profile(profile:schemas.UserProfileCreate,
                        db: Session = Depends(get_db),
                        current_user: int = Depends(Oauth2.get_current_user)):
    print(current_user.id)
    
    
    old_profile = db.query(models.UserProfile).filter(models.UserProfile.owner_id == current_user.id).first()
    if old_profile is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Profile for User with email {old_profile.owner.email} already exists"
        )
            
    new_profile = models.UserProfile(owner_id=current_user.id, **profile.dict())

    
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return(new_profile)