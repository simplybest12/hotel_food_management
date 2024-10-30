from fastapi import FastAPI,APIRouter,HTTPException,status,UploadFile,File
from models import hotels as hotel_model
from database.db import hotel_collection
from serializer.serialize import decode_document,decode_documents
from bson import ObjectId
from cloudinary.uploader import upload

router = APIRouter(
    tags = {"Hotels"},
    prefix = "/hotels"
)

def decode_hotel(hotel) -> dict:
    hotel_fields = ["id","hotel_owner","image", "name", "address", "phone_number", "foods", "ratings", "average_ratings"]
    return decode_document(hotel, hotel_fields)

def decode_hotels(hotels):
    hotel_fields = ["id","hotel_owner", "image","name", "address", "phone_number", "foods", "ratings", "average_ratings"]
    return decode_documents(hotels, hotel_fields)



@router.post("/create_hotel",status_code=status.HTTP_201_CREATED)

async def create(hotel_data : hotel_model.Hotel):
    existing_hotel =  hotel_collection.find_one( {"phone_number": hotel_data.phone_number})
    if existing_hotel:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail="Hotel exists with the same number")
    hotel_dict = hotel_data.dict()
    # try:
    #     upload_result = upload(image.file)
    #     file_url = upload_result['secure_url']
    #     hotel_dict["image"] = file_url
    # except Exception as e:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
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



