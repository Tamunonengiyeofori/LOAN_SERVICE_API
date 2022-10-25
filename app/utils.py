# PASSWORD_HASHING
from passlib.context import CryptContext

pswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_pswd, hashed_pswd):
    return pswd_context.verify(plain_pswd, hashed_pswd)

def hash_passowrd(password:str):
    return pswd_context.hash(password)