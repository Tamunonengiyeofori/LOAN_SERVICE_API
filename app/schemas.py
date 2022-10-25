from __future__ import annotations
from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List, ForwardRef
from datetime import datetime


# USER VALIDATION SCHEMAS
class UserBase(BaseModel):
    email : EmailStr
    is_active: bool = False
    is_admin: bool = False
    profile: Optional[UserProfileOut] = None
       
    class Config:
        orm_mode = True    

# class UserOut(BaseModel):
#     id: Optional[int]

class UserCreate(UserBase):
    password: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase):
    id : int
    created_at: datetime


LoanResponse = ForwardRef("LoanResponse")
# USER PROFILE VALIDATION SCHEMAS
class UserProfileBase(BaseModel):
    loans: Optional[LoanResponse] = None
    class Config:
        orm_mode = True
        
UserProfileBase.update_forward_refs()


class UserProfileCreate(BaseModel):
    name: str
    gender: str
    address: str
    mobile: constr(min_length=11)

UserOut =  ForwardRef("UserOut")

class UserProfileOut(UserProfileBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    owner_id: int
    owner: UserOut
    
UserProfileOut.update_forward_refs()


# LOAN VALIDATION SCHEMAS
class LoanBase(BaseModel):
    payment_status: int
    duration: int
    description: str
    date_paid: Optional[datetime] = None
    class Config:
        orm_mode = True
        
class LoanCreate(BaseModel):
    amount: int
    type: int
    description: str
 
class LoanResponse(BaseModel):
    id: int
    created_at : datetime
    updated_at: Optional[datetime] = None
    owner_id: int
    owner: UserProfileOut
    
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None