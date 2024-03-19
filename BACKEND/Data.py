from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

from app import User
from app import Rooms
from app import GuestHouse
from app import FoodOptions


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
objects = [Rooms(id=1, floor=0, type="D/B AC Rooms", description="Double Bed", status=st, ghId=1, pricePerDay=1000, occupancy=2, ac=1),
            Rooms(id=2, floor=0, type="D/B NON AC Rooms", description="Double Bed", status=st, ghId=1, pricePerDay=800, occupancy=2, ac=0),
            Rooms(id=3, floor=1, type="Suite Rooms", description="Single Bed", status=st, ghId=1, pricePerDay=2000, occupancy=2, ac=0),
            Rooms(id=4, floor=2, type="Meeting Room", description="", status=st, ghId=1, pricePerDay=5000, occupancy=10, ac=1),
            Rooms(id=5, floor=0, type="D/B AC Rooms", description="Double Bed", status=st, ghId=2, pricePerDay=600, occupancy=3, ac=1),
            Rooms(id=6, floor=0, type="D/B Non AC Rooms", description="Double Bed", status=st, ghId=2, pricePerDay=400, occupancy=3, ac=0),
            Rooms(id=7, floor=2, type="Dormitory Beds AC", description="Single Bed", status=st, ghId=2, pricePerDay=250, occupancy=1, ac=1)]
