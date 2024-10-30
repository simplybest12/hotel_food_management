from datetime import datetime
from database.db import otps_collection

def delete_expired_otps():
    current_time = datetime.utcnow()
    expired_otps = otp_collection.delete_many({"expires_at": {"$lt": current_time}})
    print(f"Deleted {expired_otps.deleted_count} expired OTPs")
    

    
    
    