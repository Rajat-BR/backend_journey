# Registration of a user using POST JSON request body

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class User(BaseModel):
    username: str
    age: int
    email: str

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Yo, go to the /docs "}


@app.post("/register")
def register(user: User):

    if user.age < 13:
        raise HTTPException(status_code = 400, detail = "User must be at least 13 years old")
    
    return {"message": "User registered successfully",
            "username": user.username,
            "age": user.age,
            "email": user.email}
