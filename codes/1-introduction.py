from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return {'Name':'Ayan Ahmed',
            'Goal':'AI Engineer',
            'Message':'Welcome to FastAPI AI Engineer Journey',
            'Qoute':'Always code as if the person who ends up maintaining your code will be a violent psychopath who knows where you live'}

@app.get('/hello/{name}')
def hell(name: str):
    return {'message': f'Hello, {name}'}

@app.get('/info')
def info():
    return {
        "course": "FastAPI for AI Engineers",
        "instructor": "ChatGPT-5",
        "goal": "Build scalable AI APIs"
    }

@app.get('/square/{num}')
def square(num:int):
    square = num*num
    return {'Number':num,'Square':square}