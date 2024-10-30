from bson import ObjectId
from pydantic import BaseModel, Field


class Ratings(BaseModel):
    score: int

    class Config:
        allow_population_by_field_name = True

class RatingResponse(BaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    # id:str = Field(..., alias="_id") 
    score: int
    
    
    class Config:
        allow_population_by_field_name = True