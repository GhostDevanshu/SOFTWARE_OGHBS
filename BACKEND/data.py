from flask import Flask, request, redirect, url_for, render_template,jsonify
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime, timedelta
import re

app = Flask(__name__,template_folder="/Users/devanshuagrawal/Desktop/SOFTWARE/PROJECT/FRONTEND/templates")
# MAKING THE CONNECTION
load_dotenv()
app = Flask(__name__)

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
        "name": "Dormitory Beds AC",
        "description": "Dormitory Beds rooms with AC facility available",
        "AC": 1,
        "Price_per_day": 2000,
        "floor": 0,
        "Occupancy": 1
    },
    {
        "name": "Dormitory Beds NAC",
        "description": "Dormitory Beds rooms with no AC facility available",
        "AC": 0,
        "Price_per_day": 1500,
        "floor": 1,
        "Occupancy": 1
    },
    {
        "name": "Suite Rooms",
        "description": "Special rooms available with high amounts of facilities available",
        "AC": 1,
        "Price_per_day": 3000,
        "floor": 1,
        "Occupancy": 1
    },
    {
        "name": "Double Beds NAC",
        "description": "Rooms equiped with double beds with no AC facility",
        "AC": 0,
        "Price_per_day": 2500,
        "floor": 2,
        "Occupancy": 2
    },
    {
        "name": "Double Beds AC",
        "description": "Rooms equiped with double beds with AC facility",
        "AC": 1,
        "Price_per_day": 3500,
        "floor": 2,
        "Occupancy": 2
    }
    ]

room_id = []

if (food_options.count_documents({}) == 0):
    food_options.insert_many(food_options_list)

if (room_collection.count_documents({}) == 0):
    print("working")
    room_id = room_collection.insert_many(rooms).inserted_ids