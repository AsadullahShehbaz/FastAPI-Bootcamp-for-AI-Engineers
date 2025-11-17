from fastapi import FastAPI, Request,HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

students = {"Name": "Ayan Ahmed"}


@app.get("/student/{std_id}")
async def read_item(std_id: str):
    if std_id not in students:
        raise HTTPException(status_code=404, 
                            detail="Student not found",
                            headers={"X-Error": "There goes my error"})
    return {"item": students[std_id]}

class MyException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(MyException)
async def my_exception(request:Request,exc:MyException):
    return JSONResponse(
        status_code = 418,
        content = {'message':f"Oops! {exc.name} did something. There goes a rainbow..."}
    )

@app.get('/students/{name}')
async def read_name(name : str):
    if name == 'Azan':
        raise my_exception(name=name)
    return {'Student Name : ':name}