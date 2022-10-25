from .. import models, schemas
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from ..database import get_db
from .. import models
from sqlalchemy.orm import Session
from .. import Oauth2

loan_router = APIRouter(
    prefix="/loans",
    tags = ["Loans"]
)

@loan_router.post("/", 
                  status_code=status.HTTP_201_CREATED,
                  resposne=schemas.LoanSchema)
def create_loan(loan:schemas.LoanCreate,
                db:Session = Depends(get_db)):
    ...