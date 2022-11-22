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

@loan_router.post("/",status_code=status.HTTP_201_CREATED)
def create_loan(loan:schemas.LoanCreate,
                db:Session = Depends(get_db),
                current_user: int = Depends(Oauth2.get_current_user)):
    loan_taker = db.query(models.User).filter(models.User.id == current_user.id).first()
    loan_count = len(loan_taker.loans)
    if loan_count < 1:
        new_loan = models.Loan(owner_id=current_user.id, **loan.dict())
        db.add(new_loan)
        db.commit()
        db.refresh(new_loan)
        return(new_loan)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="You Can't take more than 1 loans at a time"
    )