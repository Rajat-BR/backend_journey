# Calculator API v1
# Performs arithmetic operations using GET requests with query parameters 

from fastapi import FastAPI , HTTPException

app = FastAPI()

@app.get("/")
def home():
    return {"Message" : "Welcome to the calculator",
            "Usage" : "/calculate?operation=mode&num1=?&num2=?",
            "modes" : "[add, sub, multiply, divide]"}

@app.get("/calculate")
def calculate(operation : str, num1 : float , num2 : float):
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
        raise HTTPException(status_code = 400, detail = "Invalid Input !")
    
    return {"Operation" : operation, 
            "num1" : num1,
            "num2" : num2, 
            "Result" : result} 


