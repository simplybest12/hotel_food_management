import shortuuid
from fastapi import FastAPI,APIRouter,HTTPException,status
from models import foods as food_model
from serializer.serialize import decode_document,decode_documents
from database.db import hotel_collection
from bson import ObjectId

router = APIRouter(
    tags = {"Foods"},
    prefix = "/foods"   
)

def decode_food(food) -> dict:
    food_fields = ["id", "name", "description", "price", "quantity", "created_at", "expiry_time"]
    return decode_document(food, food_fields)

def decode_foods(foods):
    food_fields = [ "id","name", "description", "price", "quantity", "created_at", "expiry_time"]
    return decode_documents(foods, food_fields)



@router.post("/{hotel_id}/add_food",status_code=status.HTTP_201_CREATED
             ,response_model=food_model.FoodResponse)

async def add_food(hotel_id:str,food_data : food_model.Food):
    hotel = hotel_collection.find_one({"_id" : ObjectId(hotel_id)})
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Hotel with {hotel_id} not found")
    food_dict = food_data.dict()  # Convert the Pydantic model to a dictionary
    food_id = shortuuid.uuid()
    food_dict["_id"] = str(food_id)
    hotel_collection.update_one(
        {"_id": ObjectId(hotel_id)},
        {"$push": {"foods": food_dict}}  # Use $push to add the food item to the foods array
    ) 
    # print(FoodResponse(**food_dict, _id=str(hotel["_id"])))
    return food_model.FoodResponse(**food_dict)

@router.get('/{hotel_id}/fetch_food_details',status_code= status.HTTP_200_OK)

async def fetch_details(hotel_id:str):
    hotel = hotel_collection.find_one({"_id" : ObjectId(hotel_id)} , {"foods":1})
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Hotel with {hotel_id} not found")
    return {
          "status":status.HTTP_200_OK,
           "hotel_id":hotel_id,
          "foods" : decode_foods(hotel["foods"])
          }


@router.delete("/{hotel_id}/delete_food/{food_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_food(hotel_id: str, food_id: str):
    result = hotel_collection.find_one_and_update(
        {"_id": ObjectId(hotel_id)},
        {"$pull": {"foods": {"_id": food_id}}},  
        return_document=True
    )

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with {hotel_id} not found")
    
    return {"message": "Food item deleted successfully"}

    