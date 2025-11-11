from pydantic import BaseModel, Field, computed_field,field_validator
from typing import Literal, Annotated
# from config.city_tier import tier1_cities,tier2_cities

# Input schema
class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the person")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the person")]
    height: Annotated[float, Field(..., gt=0, description="Height of the person")]
    income_lpa: Annotated[float, Field(..., gt=0, description="Income of the person")]
    smoker: Annotated[bool, Field(..., description="Smoking status of the person")]
    city: Annotated[str, Field(..., description="City of the person")]
    occupation: Annotated[
        Literal['retired', 'unemployed', 'business_owner', 'government_job'],
        Field(..., description="Occupation of the person")
    ]

    @field_validator('city')
    @classmethod
    def normalize_city(cls,v:str)->str:
        v = v.strip().title()
        return v
    @computed_field
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

    @computed_field
    def age_group(self) -> str:
        if self.age < 18:
            return 'child'
        elif self.age < 25:
            return 'young'
        elif self.age < 35:
            return 'middle_aged'
        else:
            return 'senior'

    @computed_field
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return 'high'
        elif self.smoker or self.bmi > 27:
            return 'medium'
        else:
            return 'low'

    @computed_field
    def city_tier(self) -> int:
        if self.city == 'Mumbai':
            return 2
        elif self.city == 'Bangalore':
            return 2
        else:
            return 1