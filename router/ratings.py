from fastapi import FastAPI,APIRouter,HTTPException,status
from models import ratings as rating_model
from database.db import hotel_collection
from bson import ObjectId

router = APIRouter(
    tags = {"Ratings"},
    prefix = "/ratings"
    
)


@router.post("/{hotel_id}/{user_id}/add_food",status_code=status.HTTP_201_CREATED)

async def add_food(hotel_id:str,user_id:str,rating_data : rating_model.Ratings):
    hotel = hotel_collection.find_one({"_id" : ObjectId(hotel_id)})
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Hotel with {hotel_id} not found")
    rate_dict = rating_data.dict()  # Convert the Pydantic model to a dictionary
    rate_dict["user_id"] = user_id
    hotel_collection.update_one(
        {"_id": ObjectId(hotel_id)},
        {"$push": {"ratings": rate_dict}}  # Use $push to add the food item to the foods array
    ) 
    # print(FoodResponse(**rate_dict, _id=str(hotel["_id"])))
    # Fetch the updated hotel document to get the full ratings array
    updated_hotel = hotel_collection.find_one({"_id": ObjectId(hotel_id)})
    
    # Calculate the average rating
    ratings = updated_hotel["ratings"]
    total_ratings = len(ratings)
    average_rating = sum(rating["score"] for rating in ratings) / total_ratings
    average_rating = round(average_rating,1)
    
    # Update the hotel document with the new average rating
    hotel_collection.update_one(
        {"_id": ObjectId(hotel_id)},
        {"$set": {"average_ratings": average_rating}}  # Set the new average rating
    )
    
    # Return the response with the added rating and updated average rating
    return {
        "new_rating": rating_model.RatingResponse(**rate_dict, _id=str(hotel["_id"])),
        "average_rating": average_rating
    }