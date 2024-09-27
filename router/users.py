from fastapi import FastAPI,APIRouter,HTTPException,status
from models import users as user_model
from database.db import user_collection
from serializer.serialize import decode_document,decode_documents
from bson import ObjectId

router = APIRouter(
    tags = {"Users"},
    prefix = '/users'
)

def decode_user(user) -> dict:
    user_fields = ["id", "name", "age", "gender", "roles", "email", "phone_number"]
    return decode_document(user, user_fields)

def decode_users(users):
    user_fields = ["id", "name", "age", "gender", "roles", "email", "phone_number"]
    return decode_documents(users, user_fields)



@router.post('/create_users', response_model=user_model.UserResponse)
async def create_user(user_data: user_model.User):
    # Check if a user with the same email or phone number already exists
    existing_user =  user_collection.find_one({"$or": [{"email": user_data.email}, {"phone_number": user_data.phone_number}]})

    if existing_user:
        # Raise an HTTPException instead of returning it
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User exists with the same number or email ID")
    
    user_dict = user_data.dict()
    
    # Insert into MongoDB and get the inserted ID
    insert_result =  user_collection.insert_one(user_dict)
    
    # Retrieve the inserted document using the generated `_id`
    result_user =  user_collection.find_one({"_id": insert_result.inserted_id})
    
    # Ensure MongoDB document has been found
    if result_user:
        # Convert ObjectId to string
        result_user["_id"] = str(result_user["_id"])  
        # Return the document as a response model
        return user_model.UserResponse(**result_user)
    
    # If the document was not found
    raise HTTPException(status_code=400, detail="User creation failed")

@router.get('/fetch_user/{id}',status_code=status.HTTP_200_OK)

async def fetch_user(id:str):
    user = user_collection.find_one({"_id":ObjectId(id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    decode_data = decode_user(user)
    return {
        "status" : "success",
        "data" : decode_data
    }

@router.get('/fetch_users',status_code=status.HTTP_200_OK)
async def fetchusers():
    users  = user_collection.find()
    decode = decode_users(users)
    return decode


@router.delete('/delete_user/{id}',status_code=status.HTTP_204_NO_CONTENT)

async def deleteBlog(id:str):
    user = user_collection.find_one({"_id":ObjectId(id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_collection.find_one_and_delete({"_id" : ObjectId(id)})
    return {
        "message" : "Blog deleted successfully"
    }