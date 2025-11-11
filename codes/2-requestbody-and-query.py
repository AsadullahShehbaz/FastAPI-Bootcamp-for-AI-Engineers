from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI(title='Topic 3 : Request Body & Parameters')

class User(BaseModel):
    name:str
    age:int
    school_class:int
@app.post('/create_user')
def create_user(user:User):
    return {"message": "User created successfully!", "data": user}

@app.get('/')
def home():
    return {'Name':'Ayan Ahmed',
            'Goal':'AI Engineer'}

@app.get('/user/{userid}')
def user(userid:int):
    return {'User Id':userid}

@app.get('/search')
def search_user(name:str,active:bool):
    return {'Name':name,'Active':active}


