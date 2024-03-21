from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()
DB_URI = os.getenv('DB_URI')
client = MongoClient(DB_URI)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['OGHBS']

users_collection = db['USERS']
rooms_collection = db['ROOMS']
food_collection = db['FOOD']
admin = {
            "ID":0, 
            "NAME":"admin",
            "USERNAME":"admin",
            "PASSWORD":"admin",
            "ADDRESS":"", "AGE":21,
            "GENDER": "Male",
            "ROLL_NO.":""
        }
