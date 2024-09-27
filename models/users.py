from typing import Optional,List
from pydantic import BaseModel,Field
from enum import Enum


class Gender(str,Enum):
    male = "male"
    female = "female"
    
class Role(str,Enum):
    admin = "admin"
    user = "user"
    student = "student"
    NGO = "NGO"
    
class User(BaseModel):
    name: str
    age: int
    gender: Gender
    roles: List[Role]   
    email: str
    phone_number: str
    password:str

class UserResponse(BaseModel):
    id: str = Field(..., alias="_id")  # Use alias to map `_id` from MongoDB to `id`
    name: str
    age: int
    gender: Gender
    roles: List[Role]   
    email: str
    phone_number: str


    class Config:
        populate_by_name = True
    
