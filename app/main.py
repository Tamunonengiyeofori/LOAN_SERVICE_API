from fastapi import FastAPI
from app.routes.user import user_router
from app.routes.auth import auth_router
from app.routes.profile import profile_router
from app.routes.loan import loan_router
# from fastapi_jwt_auth import AuthJWT


# create an instance of the fastapi class
app = FastAPI()

from .config import settings

# @AuthJWT.load_config
# def get_config():
#     return settings.authjwt_secret_key


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(loan_router)
# if __name__ == '__main__':
#     uvicorn.run("main:app", host="localhost", port=8000)

@app.get("/")
def root():
    return{"message":"WELCOME TO THE LOAN SERVICE API "}