import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime, timedelta
load_dotenv()
# LOADING THE DATABASE
DB_URI = os.getenv('DB_URI')
client = MongoClient(DB_URI)

db = client.OGHBSdatabase

room_collection = db.room_collection
user_collection = db.user_collection
booking_collection = db.booking_collection
guest_house_collections = db.guest_house_collection
food_options = db.food_options

food_options_list = [
    {
        "description" : "Veg food (single person)",
        "Price": 200,
    },
    {
        "description" : "Non Veg Food (single person)",
        "Price": 300,
    },
    {
        "description" : "Non Veg Food (single person, fish included)",
        "Price": 380,
    },
    {
        "description" : "Non Veg Food (single person, egg included)",
        "Price": 340,
    },
    {
        "description" : "No food required",
        "Price": 0,
    }
]

rooms = [
    {   
        "code": "DR AC",
        "description": "Dormitory rooms with AC facility available",
        "AC": 1,
        "Price_per_day": 2000,
        "floor": 0,
        "Occupancy": 1
    },
    {   
        "code": "DR NAC",
        "description": "Dormitory rooms with no AC facility available",
        "AC": 0,
        "Price_per_day": 1500,
        "floor": 1,
        "Occupancy": 1
    },
    {
        "code": "SR AC",
        "description": "Special rooms available with high amounts of facilities available",
        "AC": 1,
        "Price_per_day": 3000,
        "floor": 1,
        "Occupancy": 1
    },
    {
        "code": "DBS NAC",
        "description": "Rooms equiped with double beds with no AC facility",
        "AC": 0,
        "Price_per_day": 2500,
        "floor": 2,
        "Occupancy": 2
    },
    {
        "code": "DBS AC",
        "description": "Rooms equiped with double beds with AC facility",
        "AC": 1,
        "Price_per_day": 3500,
        "floor": 2,
        "Occupancy": 2
    }
    ]

guest_houses = [
    {
        "code" : "TGH",
        "name" : "Technology Guest House",
        "address": "IIT, Guest House Rd, IIT Kharagpur, Kharagpur, West Bengal 721302, India",
        "email": "tgh@hijli.iitkgp.ernet.in",
        "contact": "+ 91-3222-282800",
        "rooms": {
            "DR AC" : 3,
            "DR NAC" : 6,
            "DBS AC" : 2
        },
        "prev_bookings":{

        }
    },
    {
        "code" : "VGH",
        "name" : "Visveswaraya Guest House",
        "address": "IIT Kharagpur Campus Kharagpur 721302",
        "email": "vgh@hijli.iitkgp.ac.in",
        "contact": "+ 91-3222-282880",
        "rooms": {
            "DR AC" : 3,
            "DBS NAC" : 6,
            "DBS AC" : 2
        },
        "prev_bookings":{

        }
    },
    {
        "code" : "KGH",
        "name" : "Kolkata Guest House",
        "address": "IIT Kharagpur Kolkata Campus,HC Block, Sector – III,Salt Lake City,Kolkata – 700106",
        "email": "tgh@hijli.iitkgp.ernet.in",
        "contact": "+ 91-3222-282834",
        "rooms": {
            "DR AC" : 3,
            "DR NAC" : 6,
            "DBS AC" : 2
        },
        "prev_bookings":{

        }
    },
]

admin = {
    "username": "admin",
    "password": "admin"
}

if (food_options.count_documents({}) == 0):
    food_options.insert_many(food_options_list)

if (room_collection.count_documents({}) == 0):
    room_collection.insert_many(rooms)

if (guest_house_collections.count_documents({}) == 0):
    guest_house_collections.insert_many(guest_houses)

if (user_collection.count_documents({}) == 0):
    user_collection.insert_one(admin)

def reset():
    db["food_options"].drop()
    db["room_collection"].drop()
    db["guest_house_collection"].drop()

    food_options.insert_many(food_options_list)
    room_collection.insert_many(rooms)
    guest_house_collections.insert_many(guest_houses)

reset()
# test space
    
prev_bookings = {
    "2024-03-29":{
        "DBS AC": 0,
        "DBS NAC": 0,
        "DR AC": 0
    },
    "2024-04-05":{
        "DBS AC": 0,
        "DBS NAC": 2,
        "DR AC": 0
    }
}
guest_house_collections.update_one({"code":"VGH"},{'$set': {'prev_bookings': prev_bookings}})