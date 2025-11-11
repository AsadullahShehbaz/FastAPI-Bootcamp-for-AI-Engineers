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

# To save model in python dictionay  , use the model dump method 
temp = std.model_dump()
print(temp)
print(type(temp))

# To save model in json  , use the model dump json method 
temp1 = std.model_dump_json()
print(temp1)
print(type(temp1))

# To save only some fields  , use the model dump  method 
temp2 = std.model_dump(include={'name','age'})
print(temp2)
print(type(temp2))

# exclude_unset is used to exclude fields that are not set in the model
temp3 = std.model_dump(exclude_unset=True)
print(temp3)
print(type(temp3))