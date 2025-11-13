import os
import logging
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional

# Step 1: Create logs directory
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# Step 2: Setup logger
logger = logging.getLogger('school_app')
logger.setLevel(logging.DEBUG)

# Step 3: Create handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

log_file_path = os.path.join(log_dir, 'school_app.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)

# Step 4: Create formatter and set it to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Step 5: Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Initialize FastAPI app
app = FastAPI()

# Sample in-memory student data
students = [
    {"id": 1, "name": "Arsal", "school_code": "SCH001"},
    {"id": 2, "name": "Ayan", "school_code": "SCH002"},
    {"id": 3, "name": "Abdullah", "school_code": "SCH001"},
    {"id": 4, "name": "Zohan", "school_code": "SCH003"},
    {"id": 5, "name": "Ibrahim", "school_code": "SCH002"},
]

@app.get("/")
def read_root():
    logger.info("Root endpoint called")
    return {"message": "Welcome to School Students Management API"}

@app.get("/students/", response_model=List[dict])
def get_students(
    skip: int = 0,
    limit: int = 3,
    q: Optional[str] = Query(None, min_length=1, max_length=50)
):
    logger.info(f"Get students called with skip={skip}, limit={limit}, query={q}")
    
    filtered_students = students
    if q:
        filtered_students = [s for s in students if q.lower() in s["name"].lower()]
        logger.debug(f"Filtered students count: {len(filtered_students)}")

    paginated_students = filtered_students[skip : skip + limit]
    logger.info(f"Returning {len(paginated_students)} students")
    
    return paginated_students

@app.get("/students/{student_id}")
def get_student(student_id: int):
    logger.info(f"Get student by id called: {student_id}")
    for student in students:
        if student["id"] == student_id:
            logger.debug(f"Student found: {student}")
            return student
    logger.error(f"Student with id {student_id} not found")
    raise HTTPException(status_code=404, detail="Student not found")

@app.post("/students/")
def add_student(name: str, school_code: str):
    new_id = max(s["id"] for s in students) + 1
    new_student = {"id": new_id, "name": name, "school_code": school_code}
    students.append(new_student)
    logger.info(f"Added new student: {new_student}")
    return new_student
