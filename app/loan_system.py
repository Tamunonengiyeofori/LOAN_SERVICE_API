# from .models import LoanType

# def select_loan_interest(user, loan_type, amount):
#     if loan_type == LoanType.BIANNUALL

from enum import IntFlag

class Trial(IntFlag):
    TWO = 2
    THREE = 3
    FOUR = 4
    
print(Trial.TWO.value)