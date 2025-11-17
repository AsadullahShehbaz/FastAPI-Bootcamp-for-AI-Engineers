from sqlmodel import Field , SQLModel

class Student(SQLModel,table=True):
    id : int | None = Field(default = None,primary_key=True)
    name : str 
    age : int | None = None

std1 = Student(id=1, name='Ali', age=10)
std2 = Student(id=2, name='Umar', age=11)
std3 = Student(id=3, name='Usman', age=9)


from sqlmodel import Session,create_engine

engine = create_engine('sqlite:///students.db')
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(std1)
    session.add(std2)
    session.add(std3)
    session.commit()
    print('All Students data saved to db')

from sqlmodel import select 
with Session(engine) as session:
    statement = select(Student).where(Student.name=='Usman')
    std = session.exec(statement).first()
    print('Student Detail is accessed by database : \n')
    print(std)