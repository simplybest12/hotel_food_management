from jose import JWTError , jwt
from datetime import datetime,timedelta
from models import users
from database.db import user_collection
from core.config import settings
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = '/auth/login')

SECRET_KEY = settings.secret_key 
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_ACCESS_TOKEN_EXPIRE_MINUTES = settings.refresh_access_token_expire_minutes
def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def refresh_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt



def verify_access_token(token:str,credential_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        _id = payload.get("user_id")
        email = payload.get("email")
        role = payload.get("role")
        # print(type(_id))
        if email is None:
            raise credential_exception
        token_data = users.TokenData(id=_id,email=email,role=role)
    except JWTError:
        raise credential_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("Here")
    token_data = verify_access_token(token, credential_exception)
    current_user = user_collection.find_one({"email": token_data.email})
    if not current_user:
        raise credential_exception

    # Convert MongoDB ObjectId to string for the user_id field
    current_user["_id"] = str(current_user["_id"])

    return current_user

def get_current_admin_user(current_user: dict = Depends(get_current_user)):
    # Assuming roles is an array or a single value of enum types, such as "admin", "user", etc.
    # print(current_user.get("roles")[0])
    if current_user.get("roles")[0] != "admin":  # Check if "admin" is in the roles array
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
    return current_user