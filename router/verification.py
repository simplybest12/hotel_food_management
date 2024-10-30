import shortuuid
from fastapi import FastAPI,APIRouter,HTTPException,status,Depends
from bson import ObjectId
from database.db import otps_collection
from pydantic import BaseModel
from twilio.rest import Client
from datetime import datetime,timedelta
import random
from core.config import settings



router = APIRouter(
    tags = {"OTPs"}, 
)


twilio_client = Client(settings.twilio_account_sid,settings.twilio_auth_token)

class OTPModel(BaseModel):
    phone_number: str
    otp: str
    created_at : datetime
    expires_at : datetime
    
class VerifyOTP(BaseModel):
    phone_number: str
    otp: str
    
class OTP(BaseModel):
    phone_number: str
    
def generate_otp():
    return str(random.randint(100000,999999))
    

    
    
@router.post('/send-otp',status_code=status.HTTP_201_CREATED)

async def create_otp(otprequest: OTP):
    otp = "000000" 
    expires_at = datetime.now() + timedelta(seconds=20)  
    otp_data = OTPModel( 
        phone_number=otprequest.phone_number,
        otp=otp,
        created_at=datetime.now(),
        expires_at=expires_at
    )   
    otps_collection.insert_one(otp_data.dict())
    otps_collection.create_index( "expires_at" , expireAfterSeconds=0  )
    return otp_data
    # try:
    #     message = twilio_client.messages.create(
    #         body=f"Your OTP is: {otp}",
            # from_=settings.twilio_phone_number,
    #         to=otprequest.phone_number
    #     )
    #     otps_collection.insert_one(otp_data.dict())
    #     return {"message": "OTP sent successfully", "sid": message.sid}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    

@router.post('/verify-otp')
async def verify_otp(verification: VerifyOTP):
    # Fetch the OTP record from the database using both the OTP and phone number
    otp_record = otps_collection.find_one({
        "otp": verification.otp,
        "phone_number": verification.phone_number
    })

    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid OTP or phone number.")

    # Check if the OTP is expired
    if otp_record['expires_at'] < datetime.now():
        otps_collection.delete_one({"_id": otp_record["_id"]})
        raise HTTPException(status_code=400, detail="OTP has expired.")
    
    otps_collection.delete_one({"_id": otp_record["_id"]})

    # If OTP is valid and not expired, proceed with your logic
    return {"message": "OTP verified successfully."}