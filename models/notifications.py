from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BroadcastNotification(BaseModel):
    title: str
    message: str
    created_at:Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    
class PersonalNotification(BroadcastNotification):
    read : bool = False
    
    class Config:
        from_attributes=True
        populate_by_name = True