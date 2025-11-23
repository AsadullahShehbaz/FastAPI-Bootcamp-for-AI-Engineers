from typing import Annotated
from fastapi import Depends , FastAPI

app = FastAPI()

async def student(name: str , age : int):
    return {'Name' : name , 'Age' : age}

@app.get('/student')
async def read_student(student_detail : str = Depends(student)):
    return {'Name' : student_detail['Name'] , 'Age' : student_detail['Age']}


class StudentClass:
    def __init__(self , name : str , age : int):
        self.name = name
        self.age = age

from typing import Annotated
@app.get('/student_class')
async def read_student(student_detail : Annotated[StudentClass,Depends()]):
    return {'Name' : student_detail.name , 'Age' : student_detail.age}


