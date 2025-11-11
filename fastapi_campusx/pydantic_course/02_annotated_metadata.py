from pydantic import BaseModel,Field , EmailStr,AnyUrl
from typing import List , Dict , Optional , Annotated

# Top 3 Benefits of pydantic :
# 1.Custom Data type Validation
# 2.Metadata can be added to the variables
# 3. Default values can be assigned to the variables
class Patient(BaseModel): # Step 1 : Create the pydanitc class and define rules
    name : Annotated[str,Field(max_length=10,title='Name of Patient',description='Please Enter the Name of Patient less than 50 characters ',examples = ['Asadullah','Ayan'])]
    email : EmailStr
    age : Annotated[int , Field(gt=0,lt=120)]
    linkedin_url : AnyUrl
    weight : Annotated[float , Field(gt=0,strict=True)]
    married : Annotated[bool,Field(default=None,description='Is the patient Married or not ?')]
    allergies : Annotated[Optional[List[str]] ,Field(default=None,max_length=5)]
    contact_details : Annotated[Dict[str,str],Field(description='Please Enter the Contact Details of Patient')]

def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.email)
    print(patient.linkedin_url)
    print(patient.age)
    print(patient.weight)
    print(patient.allergies)
    print(patient.contact_details)
    print("Inserted ")


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





# This class definition creates a `Patient` model with the following attributes and validation rules:

# * `name`: 
# 	+ Must be a string
# 	+ Has a maximum length of 10 characters
# 	+ Has a title and description for documentation purposes
# 	+ Provides example values
# * `email`: 
# 	+ Must be a valid email address
# * `age`: 
# 	+ Must be an integer
# 	+ Must be greater than 0 and less than 120
# * `linkedin_url`: 
# 	+ Must be a valid URL
# * `weight`: 
# 	+ Must be a float
# 	+ Must be greater than 0
# * `married`: 
# 	+ Must be a boolean
# 	+ Has a default value of None
# 	+ Has a description for documentation purposes
# * `allergies`: 
# 	+ Must be a list of strings (or None)
# 	+ Has a maximum length of 5 items
# 	+ Has a default value of None
# * `contact_details`: 
# 	+ Must be a dictionary with string keys and values
# 	+ Has a description for documentation purposes