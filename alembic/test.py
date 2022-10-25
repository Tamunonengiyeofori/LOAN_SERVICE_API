from datetime import date
from enum import IntFlag

class greeting:
    def __init__(self, name, age, date):
        self.name = name
        self.age = age 
        self.today = date
        
    @classmethod
    def greet_user(cls, name, age, date):
        return cls(name, age, date)
    
greet_user_1 = greeting.greet_user("Kennedy", 21, date.today())

# print(greet_user_1.today)


class LoanType(IntFlag):
    QUATERLY = 1
    BIANNUALL = 2
    ANNUAL = 3
    
    @classmethod
    def calculate_interest(cls):
        return
    