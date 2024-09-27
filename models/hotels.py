from typing import Optional,List
from pydantic import BaseModel,Field
from models.foods import Food
from models.ratings import Ratings



class Hotel(BaseModel):
    # id: str = Field(..., alias="_id") 
    name: str
    address: str
    contact_info: str
    foods : List[Food] = []
    ratings: List[Ratings] = []
    average_ratings: float = 0
    
    class config:
        populate_by_name = True