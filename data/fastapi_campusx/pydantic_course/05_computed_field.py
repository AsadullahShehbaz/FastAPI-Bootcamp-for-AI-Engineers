from pydantic import BaseModel,computed_field

class Patient(BaseModel):
    name : str
    email : str
    age : int
    weight : float
    height : float

    @computed_field
    def bmi(self)-> float:
        return round(self.weight/(self.height**2),2)

patient_info = {
    'name':'Asadullah',
    'email':'asadullah@gmail.com',
    'age':10,
    'weight':50,
    'height':1.5
}
patient1 = Patient(**patient_info)

print(patient1.bmi)