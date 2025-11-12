from pydantic import BaseModel , Field , EmailStr , AnyUrl,field_validator
from typing import List , Dict , Optional , Annotated

class Patient(BaseModel):
    name : str
    email : EmailStr 
    age : int 
    weight : float 
    married : bool 
    @field_validator('email')
    # @classmethod
    def email_validator(cls,value):
        valid_domains = ['hdfc.com','icic.com','gmail.com']
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain ')
        return value 
    @field_validator('name')
    # @classmethod
    def transform_name(cls,value):
        return value.upper()
    @field_validator('age')
    def check_age(cls,value):
        if value<0:
            raise ValueError('Age cannot be negative')
        return value

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
    'married':False
}
patient1 = Patient(**patient_info)

update_patient_data(patient1)