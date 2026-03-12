from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message" : "Hello World"}


@app.get("/home/{name}")
def greet(name):
    return {"message" : f"Hello {name}"}

@app.get("/square")
def square(num : int):
    return {"Square" : num*num}