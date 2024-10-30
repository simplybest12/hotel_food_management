from fastapi import FastAPI,APIRouter,HTTPException,status,UploadFile,File,Depends
from models import order as order_model
from models.order import DeliveryAddress
from database.db import hotel_collection
from serializer.serialize import decode_document,decode_documents
from bson import ObjectId
from cloudinary.uploader import upload
from datetime import datetime,timedelta
from database.db import order_collection
from oauth2 import get_current_user

router = APIRouter(
    tags = {"Orders"},
    prefix = "/order"
)

# def decode_order(hotel) -> dict:
#     hotel_fields = ["id","hotel_owner","image", "name", "address", "phone_number", "foods", "ratings", "average_ratings"]
#     return decode_document(hotel, hotel_fields)

# def decode_orders(hotels):
#     hotel_fields = ["id","hotel_owner", "image","name", "address", "phone_number", "foods", "ratings", "average_ratings"]
#     return decode_documents(hotels, hotel_fields)



@router.post('/new_order/{hotel_id}', status_code=status.HTTP_201_CREATED)
async def new_order(
    hotel_id: str,
    order_request: order_model.CreateOrderRequest,
    current_user:dict =  Depends(get_current_user)
):
    customer_id = current_user["_id"]
    delivery_address = current_user["address"]
    total_amount = sum(item.price * item.quantity for item in order_request.order_items)

    # Create an Order instance
    order = order_model.Order(
        customer_id=customer_id,
        hotel_id=hotel_id,
        order_items=order_request.order_items,  # Directly use the items
        total_amount=total_amount,
        estimated_delivery_time=datetime.utcnow() + timedelta(minutes=30),
        address=DeliveryAddress(**delivery_address)  # Ensure this matches your DeliveryAddress model
    )

    # Insert the order into the database
    result = order_collection.insert_one(order.dict(by_alias=True))

    return order
