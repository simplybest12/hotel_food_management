
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import urllib.parse
from core.config import settings

username = urllib.parse.quote_plus(settings.mongo_user)
password = urllib.parse.quote_plus(settings.mongo_password)
uri = f"mongodb+srv://{username}:{password}@init.ua4q3.mongodb.net/?retryWrites=true&w=majority&appName={settings.app_name}"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.hotel_management_system
user_collection = db["users"]
hotel_collection = db["hotels"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)