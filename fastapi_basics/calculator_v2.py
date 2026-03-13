# Calculator API v2
# Uses Pydantic models to validate and parse JSON request body
# Calculator API v2 accepts calculation requests via POST with JSON body

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Calculation(BaseModel):
    operation : str
    num1 : float
    num2 : float

@app.get("/")
def home():
    return {"message" : "Yo, go to the /docs"}

@app.post("/calculate")
def calculate(data : Calculation):
    operation = data.operation
    num1 = data.num1
    num2 = data.num2

    if operation == "add":
        result = num1 + num2
    elif operation == "sub":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        if num2 == 0:
            raise HTTPException(status_code = 400, detail = "Cannot divide number by 0 !")
        result = num1 / num2
    else:
        raise HTTPException(status_code = 400, detail = "Invalid Operation !")
    
    return {"operation" : operation,
            "num1" : num1,
            "num2" : num2, 
            "result" : result}