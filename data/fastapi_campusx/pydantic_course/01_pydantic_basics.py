from pydantic import BaseModel,Field , EmailStr,AnyUrl
from typing import List , Dict , Optional

class Patient(BaseModel): # Step 1 : Create the pydanitc class and define rules
    email : EmailStr
    name : str = Field(max_length=10)
    age : int = Field(gt=0,lt=120)
    linkedin_url : AnyUrl
    weight : float = Field(gt=0)
    married : bool = False
    allergies : Optional[List[str]] =Field(max_length=5)
    contact_details : Dict[str,str]

def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.email)
    print(patient.linkedin_url)
    print(patient.age)
    print(patient.weight)
    print(patient.allergies)
    print(patient.contact_details)
    print("Inserted ")

def update_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.allergies)
    print(patient.contact_details)
    print("Updated ")
patient_info = {
    'email':'abc@gmail.com',
    'name':'Asadullah',
    'age':21,
    'linkedin_url':'http://linkedin.com',
    'weight':50.5,
    'married':True,
    'allergies':['Pollen','dust','cats'],
    'contact_details':{'phone':'136100','email':'abc@xyz.com'}
    }

patient1 = Patient(**patient_info) # Step 2 : Create object of pydantic class


insert_patient_data(patient1) # Step 3 : Send pydantic object to function

patient1.age = 22
# update_patient_data(patient1)