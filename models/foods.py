from typing import Optional,List
from pydantic import BaseModel,Field
from datetime import date,datetime

class Food(BaseModel):
    _id:str
    name: str
    description:str
    price:str
    quantity: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expiry_time : datetime
    
    class Config:
        arbitrary_types_allowed = True
    

class FoodResponse(Food):
    id: str = Field(..., alias="_id") 
    
    class Config:
        from_attributes:True
    
    
    
            
    