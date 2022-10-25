from sqlalchemy import TIME, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import relationship
from .database import Base
from enum import IntFlag

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    email =  Column(String(80), nullable=False, unique=True)
    password = Column(String(100), nullable=False)   
    is_active = Column(Boolean, server_default="False", nullable=False)
    is_admin = Column(Boolean, server_default="False", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=text("now()"))
    profile = relationship("UserProfile", back_populates="owner", uselist=False)
    
    def __repr__(self):
        return f"{self.email}"
    
class UserProfile(Base):
    __tablename__ = "user_profile"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(80), nullable=False)
    gender = Column(String(80), nullable=False)
    address = Column(String(250), nullable=False)
    mobile = Column(String(80), nullable=False)
    loans = relationship("Loan", back_populates="owner")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=text("now()"))
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, unique=True)
    owner = relationship("User", back_populates="profile")
    
class LoanType(IntFlag):
    QUATERLY = 1
    BIANNUALL = 2
    ANNUAL = 3
    
class DurationType(IntFlag):
    THREE_MONTHS = 1
    SIX_MONTHS = 2
    TWELVE_MONTHS = 3
    

class PaymentStatus(IntFlag):
    PAID = 1
    DEBT = 2
    PAYING = 3
    
class Loan(Base):
    __tablename__ = "loan"
    id = Column(Integer, primary_key=True, nullable=False)
    amount = Column(Integer, default=0, nullable=False)
    type = Column(ChoiceType(LoanType, impl=Integer()), nullable=False)
    payment_status = Column(ChoiceType(PaymentStatus, impl=Integer()), default=PaymentStatus.DEBT.value, nullable=False)
    # duration = Column(ChoiceType(DurationType, impl=Integer()))
    duration = Column(Integer, default=0, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=text("now()"))   
    description = Column(String(255), nullable=False)
    date_paid = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=text("now()"))
    owner_id = Column(Integer, ForeignKey("user_profile.id", ondelete="CASCADE"))
    owner = relationship("UserProfile", back_populates="loans")
    
    def __repr__(self):
        return f"{self.id} {self.type}"
