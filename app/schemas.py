from __future__ import annotations
from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List, ForwardRef
from datetime import datetime
from app.models import LoanType

 



# USER VALIDATION SCHEMAS
class UserCreate(BaseModel):
    email: EmailStr
    is_admin: Optional[bool] = False
    is_active: Optional[bool] = False
    password: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    

# LOAN VALIDATION SCHEMAS
class LoanCreate(BaseModel):
    amount: int
    type: LoanType 
    description: str



class LoanResponse(BaseModel):
    id: int
    payment_status: int
    date_paid: Optional[datetime] = None
    created_at : datetime
    updated_at: Optional[datetime] = None
    owner_id: int
    owner: Optional[UserOut] = None
    
    class Config:
        orm_mode = True




class UserOut(BaseModel):
    id : int
    email : EmailStr
    is_active: bool = False
    is_admin: bool = False
    created_at: datetime
    profile: Optional[UserProfileOut] = None
    loans: Optional[List[LoanResponse]] = None
    class Config:
        orm_mode = True  



# USER PROFILE VALIDATION SCHEMAS
class UserProfileCreate(BaseModel):
    name: str
    gender: str
    address: str
    mobile: constr(min_length=11)


class UserProfileOut(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: int
    owner: Optional[UserOut] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None