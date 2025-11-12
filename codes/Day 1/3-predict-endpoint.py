from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def home():
    return {
        'Name':'Ayan Ahmed',
        'Goal':'AI Engineer'
    }

class PredictionInput(BaseModel):
    age:int 
    income:int

@app.post('/predict')
def predict(input:PredictionInput ,verbose:bool=False):
    """
    Example /predict API that mimics ML model prediction
    Body: {"age": 25, "income": 50000}
    Query Param: verbose=true
    """
    if input.age < 15 and input.income > 1000:
        prediction = 'You are students'
    else:
        prediction = 'You are not students'

    if verbose:
        return {
            'Input':input,
            'Inference':prediction,
            'Confidence':0.99
        }
    return {
        'Inference':prediction
    }