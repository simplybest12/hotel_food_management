from fastapi import FastAPI,APIRouter,HTTPException,status,Depends,Request
from models import notifications,users as user_model
from database.db import user_collection
from serializer.serialize import decode_document,decode_documents
import asyncio
from bson import ObjectId
from oauth2 import get_current_admin_user,get_current_user
from core.utils import hash
from sse_starlette.sse import EventSourceResponse
from models import ssemodel as event_model 
from models.ssemodel import SSEEvent

router = APIRouter(
    tags = {"Admin"},
    prefix = '/admin'
)

def decode_user(user) -> dict:
    user_fields = ["id", "name" ,"gender", "roles", "email", "phone_number"]
    return decode_document(user, user_fields)

def decode_users(users):
    user_fields = ["id", "name","gender", "roles","email", "phone_number"]
    return decode_documents(users, user_fields)


@router.post("/emit")
async def new_event(event:event_model.EventModel):
    SSEEvent.add_event(event)
    return {"message": "Event added","count":SSEEvent.count()}

@router.get('/stream')
async def stream( req:Request):
    async def stream_generator():
        while True:
            if await req.is_disconnected():
                print("SSE Disconnected")
                return
            event =  SSEEvent.get_event()
            if event:
                yield f"data: {event}\n\n"
            await asyncio.sleep(0.5)

    return EventSourceResponse(stream_generator())
                
        
    






@router.post('/create', response_model=user_model.UserResponse)
async def create_user(user_data: user_model.User,current_user = Depends(get_current_admin_user)):
    existing_user =  user_collection.find_one({"$or": [{"email": user_data.email}, {"phone_number": user_data.phone_number}]})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail="User exists with the same number or email ID")
    user_dict = user_data.dict()
    user_dict["password"] = hash.Hash.bcrypt(user_data.password)
    

    insert_result =  user_collection.insert_one(user_dict)

    result_user =  user_collection.find_one({"_id": insert_result.inserted_id})

    if result_user:
        result_user["_id"] = str(result_user["_id"])
        return user_model.UserResponse(**result_user)
    raise HTTPException(status_code=400, detail="User creation failed")

@router.get('/fetch_user/{id}',status_code=status.HTTP_200_OK)

async def fetch_user(id:int,current_user = Depends(get_current_admin_user)):
    user = users_collection.find_one({"_id": ObjectId(id)}) 
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    decode_data = decode_user(user)
    return decode_data

@router.get('/fetch_users',status_code=status.HTTP_200_OK)
async def fetchusers(current_user = Depends(get_current_admin_user)):
    user_id = current_user["_id"]
    user = user_collection.find_one({"_id":ObjectId(user_id)})
    decode = decode_users(users)
    return decode


@router.delete('/delete_user/{id}',status_code=status.HTTP_204_NO_CONTENT)

async def deleteBlog(id:int,current_user = Depends(get_current_admin_user)):
   user = users_collection.find_one({"_id": ObjectId(id)})
   if not user:
       raise HTTPException(status_code=404, detail="User not found")
   user_collection.find_one_and_delete({"_id" : ObjectId(user_id)})
   return {
        "message" : "Blog deleted successfully"
    }
