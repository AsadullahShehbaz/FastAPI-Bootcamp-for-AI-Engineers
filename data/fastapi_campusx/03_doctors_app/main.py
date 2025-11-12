# ==========================================================
# 🏥 FASTAPI PATIENT MANAGEMENT APP
# ----------------------------------------------------------
# This app allows you to store, retrieve, and sort patient data
# using FastAPI 🚀. Perfect for beginners to learn APIs + Pydantic.
# ==========================================================

from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal,Optional
import json

# ----------------------------------------------------------
# 🛠️ Step 1: Create the FastAPI app instance
# ----------------------------------------------------------
# 'app' is the brain of our API – all endpoints will connect here.
app = FastAPI()

# ----------------------------------------------------------
# 📦 Step 2: Define the Pydantic model for data validation
# ----------------------------------------------------------
# Think of this as a "blueprint" for how patient data should look.
# Every request must follow these rules or it gets rejected.
class Patient(BaseModel):
    # Unique Patient ID
    id: Annotated[str, Field(..., description="ID of the Patient", examples=['P001'])]
    # Full name of the patient
    name: Annotated[str, Field(..., description="Name of the Patient", examples=['Asadullah', 'Ayan'])]
    # City where patient lives
    city: Annotated[str, Field(..., description="City where he lives", examples=['GRW'])]
    # Age must be between 1 and 119 years
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the Patient")]
    # Gender must be one of these options
    gender: Annotated[Literal['male', 'female', 'other'], Field(..., description="Gender of the Patient")]
    # Height in meters
    height: Annotated[float, Field(..., gt=0, description="Height of the Patient in meters")]
    # Weight in kilograms
    weight: Annotated[float, Field(..., gt=0, description="Weight of the Patient in kg")]

    # 🧮 Computed Field: BMI (Body Mass Index)
    @computed_field
    @property
    def bmi(self) -> float:
        # Formula: weight / height²
        return round(self.weight / (self.height ** 2), 2)

    # 🧾 Computed Field: Health Verdict
    @computed_field
    @property
    def verdict(self) -> str:
        # Classify based on BMI value
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 30:
            return "Normal"
        else:
            return "Obese"

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


# ----------------------------------------------------------
# 📂 Step 3: Utility Functions for Database Operations
# ----------------------------------------------------------
# Here we use a JSON file as a database for simplicity.
# In real life, you'd connect to a proper database.

def load_data():
    """Load all patient records from JSON file"""
    with open('patients.json', 'r') as f:
        return json.load(f)

def save_data(data):
    """Save all patient records to JSON file"""
    with open('patients.json', 'w') as f:
        json.dump(data, f)

# ----------------------------------------------------------
# 🏠 Step 4: Home Endpoint
# ----------------------------------------------------------
@app.get("/")
async def root():
    """A friendly welcome message for our API."""
    return {
        'Info': 'My first FastAPI Project with CampusX: '
                'This is the best platform to get doctors details worldwide!'
    }

# ----------------------------------------------------------
# 📜 Step 5: View All Patients
# ----------------------------------------------------------
@app.get('/view')
def view():
    """Get a full list of all patients in the database."""
    return load_data()

# ----------------------------------------------------------
# 🔍 Step 6: View a Single Patient by ID
# ----------------------------------------------------------
@app.get('/view/{patient_id}')
def view_patient(
    patient_id: str = Path(..., description='The ID of the patient to get details of', title='Patient ID', example='P001')
):
    """Retrieve data for a specific patient using their ID."""
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        # If patient doesn't exist → return 404 Not Found
        raise HTTPException(status_code=404, detail="Patient not found")

# ----------------------------------------------------------
# 📊 Step 7: Sort Patients
# ----------------------------------------------------------
@app.get('/sort')
def sort_patients(
    sort_by: str = Query(..., description='Sort on the base of height, weight, or bmi'),
    order: str = Query('asc', description='Sort in ascending or descending order')
):
    """Sort all patients by height, weight, or BMI."""
    value_fields = ['height', 'weight', 'bmi']

    # Validate sorting field
    if sort_by not in value_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by field, choose from {value_fields}")

    # Validate sorting order
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order field, choose from ['asc', 'desc']")

    data = load_data()
    sort_order = True if order == 'desc' else False

    # Sorting logic
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by), reverse=sort_order)

    return sorted_data

# ----------------------------------------------------------
# ➕ Step 8: Create a New Patient
# ----------------------------------------------------------
@app.post("/create")
def create_patient(patient: Patient):
    """Add a brand-new patient to the database."""
    data = load_data()

    # Ensure patient ID is unique
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists!")

    # Convert Pydantic model → dictionary, skip 'id' in values
    data[patient.id] = patient.model_dump(exclude=['id'])

    # Save updated data
    save_data(data)

    # Return a nice response message
    return JSONResponse(status_code=201, content={'message': 'New patient created successfully'})

# ----------------------------------------------------------
# ✏ Step 9: Update an Existing Patient
# ----------------------------------------------------------
@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
    #-> pydantic object -> dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')

    # add this dict to data
    data[patient_id] = existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail='patient not found')
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200,content={'message':'patient deleted'})