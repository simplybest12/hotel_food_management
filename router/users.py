from fastapi import FastAPI,APIRouter,HTTPException,status,Depends,UploadFile,File
from models import users as user_model
from database.db import user_collection
from serializer.serialize import decode_document,decode_documents
from bson import ObjectId
from oauth2 import get_current_admin_user,get_current_user
from core.utils import hash
import oauth2
from cloudinary.uploader import upload

router = APIRouter(
    tags = {"Users"},
    prefix = '/users'
)

def decode_user(user) -> dict:
    user_fields = ["id", "name" ,"gender", "roles", "email","address", "phone_number"]
    return decode_document(user, user_fields)

def decode_users(users):
    user_fields = ["id", "name","gender", "roles","email", "address","phone_number"]
    return decode_documents(users, user_fields)



# @router.post('/create_users', response_model=user_model.UserResponse)
# async def create_user(user_data: user_model.User):
#     # Check if a user with the same email or phone number already exists
#     existing_user =  user_collection.find_one({"$or": [{"email": user_data.email}, {"phone_number": user_data.phone_number}]})
#     if existing_user:
#         raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail="User exists with the same number or email ID")
#     user_dict = user_data.dict()
#     # upload_result = upload(image.file)
#     # file_url = upload_result['secure_url']
#     # user_dict["image"] = file_url
#     user_dict["password"] = hash.Hash.bcrypt(user_data.password)
    
#     # Insert into MongoDB and get the inserted ID
#     insert_result =  user_collection.insert_one(user_dict)
    
#     # Retrieve the inserted document using the generated `_id`
#     result_user =  user_collection.find_one({"_id": insert_result.inserted_id})
    
#     # Ensure MongoDB document has been found
#     if result_user:
#         # Convert ObjectId to string
#         result_user["_id"] = str(result_user["_id"])  
#         # Return the document as a response model
#         return user_model.UserResponse(**result_user)
    
#     # If the document was not found
#     raise HTTPException(status_code=400, detail="User creation failed")

@router.get('/fetch_user',status_code=status.HTTP_200_OK)

async def fetch_user(current_user = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    decode_data = decode_user(current_user)
    return decode_data


@router.delete('/delete_user',status_code=status.HTTP_204_NO_CONTENT)

async def deleteBlog(current_user = Depends(get_current_user)):
    user_id = current_user["_id"]
    user = user_collection.find_one({"_id":ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_collection.find_one_and_delete({"_id" : ObjectId(user_id)})
    return {
        "message" : "Blog deleted successfully"
    }
    
@router.get('/find/{phone_number}',status_code=status.HTTP_200_OK)
async def find(phone_number: str):
    user = user_collection.find_one({"phone_number": phone_number})
    if user:
        decode_data = decode_user(user)
        role = user["roles"][0]  
        access_token = oauth2.create_access_token(
            data={"user_id": str(user["_id"]), "email": user["email"], "role": role}
        )
        return {
            "success": True,
            "access_token": access_token,
            "detail":decode_data,
            "token_type": "bearer",
            "message": "User found."  
        }
    return {
        "success": False,
        "message": "Phone number not found, you can proceed with registration."
    }
@router.post("/upload")
async def handle_upload(image: UploadFile=File(...)):
    try:
        upload_result = upload(image.file)
        file_url = upload_result['secure_url']
        
        return {
            "data": {
                "url": file_url
            }
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)