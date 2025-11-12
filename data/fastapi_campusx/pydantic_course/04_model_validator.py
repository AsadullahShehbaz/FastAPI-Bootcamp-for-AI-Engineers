from pydantic import BaseModel , EmailStr,model_validator
from typing import Dict , List

class Patient(BaseModel):
    name : str
    email : EmailStr
    age : int
    weight : float
    married : bool
    allergies : List[str]
    contact_details : Dict[str,str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls,model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patient is older than 60 and must have emergency contact')
        return model
def update_patient_data(patient : Patient):
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print('Updated...')

patient_info = {
    'name':'Asadullah',
    'email':'asadullah@gmail.com',
    'age':10,
    'weight':50,
    'married':False,
    'allergies':['Pollen','dust','cats'],
    'contact_details':{'phone':'136100','email':'abc@xyz.com',
    'emergency':'1234567890'}
}
patient1 = Patient(**patient_info)

update_patient_data(patient1)