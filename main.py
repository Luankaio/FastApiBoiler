from fastapi import FastAPI
from db.database_connection import Database


app = FastAPI()

mongo_uri = "mongodb://localhost:27017"
database_name = "mydatabase"
db = Database(mongo_uri, database_name)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


