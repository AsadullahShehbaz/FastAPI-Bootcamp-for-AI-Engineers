from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import JSONResponse
import asyncio
app = FastAPI()

students_db = {
    1: {"name": "Ayan Ahmed", "age": 8, "grade": "A"},
    2: {"name": "Muhammad Arsal", "age": 9, "grade": "B"},
    3: {"name": "Hafiz Abdullah", "age": 12, "grade": "A+"}
}
@app.get('/students')
async def get_all_students():
    return {"class": 5, "total_students": len(students_db), "students": students_db}

# ✅ Route to get student by ID
@app.get("/student/{student_id}")
async def get_student(student_id: int):
    # Check if student exists
    if student_id not in students_db:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found in class 5."
        )
    return {"student_id": student_id, "details": students_db[student_id]}

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "hint": "Check your input values again.",
            "path": str(request.url)
        },
    )


@app.get('/divide')
async def divide(x:int,y:int):
    await asyncio.sleep(1)

    if y == 0 :
        raise HTTPException(status_code=400,detail="Cannot divide by zero")
    result = x/y
    return {
        "operation": f"{x} ÷ {y}",
        "result": result,
        "message": "✅ Division successful!"}


# ✅ Home route
@app.get("/")
async def home():
    return {"message": "Welcome to Class 5 School API 🏫"}