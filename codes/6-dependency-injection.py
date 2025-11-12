from typing import Annotated
from fastapi import Depends, FastAPI

# 🚀 Create a FastAPI application instance
app = FastAPI()

# 🎓 Dependency function to collect student details from query parameters
async def student(name: str | None, school_name: str | None = None, age: int = 10):
    # 📦 Return student info as a dictionary
    return {'Name of Student ': name, 'School Name of Student ': school_name, 'Age of Student': age}

# 📍 Define a GET endpoint '/student' that depends on the student() function
@app.get('/student')
async def student_detail(std: Annotated[dict, Depends(student)]):
    # 🪄 Automatically receives data from the dependency and returns it as response
    return std

Student_Model = Annotated[dict, Depends(student)]
@app.get('/student_detail')
async def student_detail(std: Student_Model):
    # 🪄 Automatically receives data from the dependency and returns it as response
    return std
