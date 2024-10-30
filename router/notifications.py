import shortuuid
from fastapi import FastAPI,APIRouter,HTTPException,status,Depends
from serializer.serialize import decode_document,decode_documents
from database.db import notification_collection,user_collection
from oauth2 import get_current_admin_user
from models import notifications as notif_model
from bson import ObjectId

router = APIRouter(
    tags = {"Notifications"},
    prefix = "/notifications"   
)

@router.post('/all_users')
async def all(notify_data:notif_model.BroadcastNotification,current_user = Depends(get_current_admin_user)):
    notify_dict = notify_data.dict()
    insert_result = notification_collection.insert_one(notify_dict)
    insert_id = str(insert_result.inserted_id)
    return {
        "status": "success",
        "message": "Notification sent to all users.",
        "notification_id": insert_id 
    }


@router.post('/user/{user_id}',status_code=status.HTTP_201_CREATED)

async def one(user_id:str,notify:notif_model.PersonalNotification,current_user=Depends(get_current_admin_user)):
    user = user_collection.find_one({"_id":ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with {user_id} not found")
    
    notify_dict = notify.dict()
    notify_dict["user_id"] = str(user_id)
    user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"personal_notification": notify_dict}} 
    ) 
    # print(FoodResponse(**food_dict, _id=str(hotel["_id"])))
    return notify_dict
    