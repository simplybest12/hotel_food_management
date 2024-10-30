from pydantic import BaseModel, Field
from enum import Enum
from models.users import DeliveryAddress
from typing import List,Optional
from datetime import datetime



class OrderStatus(str,Enum):
    PREPARING = "Preparing"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
    
class OrderItem(BaseModel):
    food_id : str
    quantity : int
    price : float
    
class CreateOrderRequest(BaseModel):
    order_items : List[OrderItem]
    
class Order(BaseModel):
    customer_id: str 
    hotel_id: str 
    order_items: List[OrderItem] 
    total_amount: float 
    order_status: OrderStatus = OrderStatus.PREPARING 
    timestamp: datetime = Field(default_factory=datetime.utcnow) 
    estimated_delivery_time: Optional[datetime]
    address: DeliveryAddress


class OrderResponse(BaseModel):
    hotel_id: str  
    order_items: List[OrderItem]  
    total_amount: float 
    order_status: OrderStatus = OrderStatus.PREPARING
    timestamp: datetime = Field(default_factory=datetime.utcnow)  # Order creation time
    estimated_delivery_time: Optional[datetime]  # Expected time of completion or delivery
    address: DeliveryAddress
    
    class Config:
        from_attributes = True
    