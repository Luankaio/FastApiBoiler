from fastapi import FastAPI
from controller.user_controller import UserController
from controller.auth_controller import UserAuthController

app = FastAPI()


app.include_router(UserAuthController.router)
app.include_router(UserController.router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


