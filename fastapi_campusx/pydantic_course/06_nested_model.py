from pydantic import BaseModel 

class Address(BaseModel):
    city : str
    state : str
    pin : str

class Student(BaseModel):
    name : str
    age : int
    gender : str = 'Male' # Default value for  gender is Male
    address : Address

address_dict = {
    'city':'Lahore',
    'state':'Punjab',
    'pin':'54000'
}
add_object = Address(**address_dict)
std_dict = {
    'name':'Asadullah',
    'age':21,
    'address': add_object
}
std = Student(**std_dict)

print(std.name)
print(std.age)
print(std.address)
