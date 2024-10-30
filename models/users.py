from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum
from models.notifications import PersonalNotification
from datetime import datetime

class Gender(str, Enum):
    male = "male"
    female = "female"

class Role(str, Enum):
    admin = "admin"
    hotel_owner = "hotel owner"
    user = "user"
    NGO = "NGO"

class RoleSignup(str, Enum):
    user = "user"
    NGO = "NGO"
    hotel_owner = "hotel owner"
    

class DeliveryAddress(BaseModel):
    address_line: str
    city: Optional[str] = None
    postal_code: Optional[str] = None
    room_number: Optional[str] = None  

class User(BaseModel):
    name: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    password: str
    gender: Gender
    roles: Role
    personal_notification: Optional[List[PersonalNotification]] = Field(default_factory=list)  # Ensure it's always a list
    address:DeliveryAddress
    email: str
    phone_number: str

class UserSignup(BaseModel):
    name: str
    gender: Gender
    roles: RoleSignup
    email: str
    phone_number: str
    personal_notification: Optional[List[PersonalNotification]] = Field(default_factory=list)  # Ensure it's always a list
    address:DeliveryAddress
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class UserResponse(BaseModel):
    id: str = Field(..., alias="_id")  # Use alias to map `_id` from MongoDB to `id`
    name: str
    gender: Gender
    roles: Role
    email: str
    phone_number: str
    # personal_notification: Optional[List[PersonalNotification]] = Field(default_factory=list)

    class Config:
        populate_by_name = True

class TokenData(BaseModel):
    id: str
    email: Optional[str] = None
    role: str
