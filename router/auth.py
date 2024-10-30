from fastapi import FastAPI,APIRouter,HTTPException,status,Depends
from models import users as user_model
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database.db import user_collection
from bson import ObjectId
import oauth2
from core.utils import hash


router = APIRouter(
    tags = {"Auth"},
    prefix = "/auth"   
)

@router.post('/login',status_code=status.HTTP_200_OK)

async def login(user_credentials: OAuth2PasswordRequestForm=Depends()):    
    existing_user = user_collection.find_one({"email":user_credentials.username})
    if not existing_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not hash.Hash.verify(user_credentials.password,existing_user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    role = existing_user["roles"][0]
    print(role)

    access_token = oauth2.create_access_token(
        data={"user_id":str(existing_user["_id"]),"email": existing_user["email"], "role": role}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/register',status_code=status.HTTP_201_CREATED)

async def register(user_data : user_model.UserSignup):
    existing_user =  user_collection.find_one({"$or": [{"email": user_data.email}, {"phone_number": user_data.phone_number}]})

    if existing_user:
        # Raise an HTTPException instead of returning it
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User exists with the same number or email ID")
    
    user_dict = user_data.dict()
    insert_result =  user_collection.insert_one(user_dict)
    result_user =  user_collection.find_one({"_id": insert_result.inserted_id})
    if result_user:
        result_user["_id"] = str(result_user["_id"])
        role = result_user["roles"][0]
        print(role)

        access_token = oauth2.create_access_token(
            data={"user_id":str(result_user["_id"]),"email": result_user["email"], "role": role}
        )  
        refresh_token = oauth2.refresh_access_token(
            data={"user_id":str(result_user["_id"]),"email": result_user["email"], "role": role}
                       
        )
        return {
            "user": user_model.UserResponse(**result_user),
            "access_token": access_token,
            "refresh_token":refresh_token
        }
    
    
    raise HTTPException(status_code=400, detail="User creation failed")
    
    


