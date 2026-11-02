from fastapi import FastAPI
app=FastAPI(title="Python CI/CD Demo",description="Learning Jenkins CI/CD pipeline",version="1.0.0")

@app.get("/")
def home():
    return {
        "application": "Python CI/CD Demo",
        "message": "Application is running",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {"status":"healthy"}

@app.get("/add/{a}/{b}")
def add_numbers(a:int,b:int):
    return {"operation":"addition","result":a+b}

@app.get("/multiply/{a}/{b}")
def multiply_numbers(a: int, b: int):
    return {
        "operation": "multiplication",
        "result": a * b
    }