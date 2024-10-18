from fastapi import FastAPI
from controller.user_controller import UserController

app = FastAPI()


app.include_router(UserController.router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


