from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Simulate a simple ORM model (e.g., a database record)
class StudentORM:
    def __init__(self, id: int, name: str, grade: str):
        self.id = id
        self.name = name
        self.grade = grade

# Pydantic model for API response with orm_mode enabled
class StudentReportCard(BaseModel):
    id: int
    name: str
    grade: str

    class Config:
        orm_mode = True  # Allow reading data directly from ORM objects

# Dummy in-memory "database"
students_db = {
    1: StudentORM(id=1, name="Ali", grade="A+"),
    2: StudentORM(id=2, name="Sara", grade="B"),
    3: StudentORM(id=3, name="Zain", grade="A"),
}

@app.get("/students/{student_id}", response_model=StudentReportCard)
async def get_student_report(student_id: int):
    student = students_db.get(student_id)
    if not student:
        return {"error": "Student not found"}
    # FastAPI uses StudentReportCard to convert ORM object to JSON automatically
    return student
