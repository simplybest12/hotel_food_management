from fastapi import FastAPI,APIRouter,HTTPException,status
from models import hotels as hotel_model
from database.db import hotel_collection
from serializer.serialize import decode_document,decode_documents
from bson import ObjectId

router = APIRouter(
    tags = {"Hotels"},
    prefix = "/hotels"
)

def decode_hotel(hotel) -> dict:
    hotel_fields = ["id", "name", "address", "contact_info", "foods", "ratings", "average_ratings"]
    return decode_document(hotel, hotel_fields)

def decode_hotels(hotels):
    hotel_fields = ["id", "name", "address", "contact_info", "foods", "ratings", "average_ratings"]
    return decode_documents(hotels, hotel_fields)



@router.post("/create_hotel",status_code=status.HTTP_201_CREATED)

async def create(hotel_data : hotel_model.Hotel):
    hotel_dict = hotel_data.dict()
    
    insert_hotel = hotel_collection.insert_one(hotel_dict)
    
    ref_id = str(insert_hotel.inserted_id)
    
    return ref_id


@router.get("/fetch_hotels",status_code=status.HTTP_200_OK)

async def fetch_details():
    hotels = hotel_collection.find()
    decoded_data = decode_hotels(hotels)
    return decoded_data

@router.get("/fetch_hotel/{hotel_id}",status_code=status.HTTP_200_OK)

async def fetch_hotel(hotel_id : str):
    hotel = hotel_collection.find_one({"_id" : ObjectId(hotel_id)})
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    decode_data = decode_hotel(hotel)
    return decode_data