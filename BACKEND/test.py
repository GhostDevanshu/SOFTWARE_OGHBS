# from flask import Flask,  jsonify, request

# app = Flask(__name__)


# @app.after_request
# def add_cors_headers(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
#     return response

# @app.route('/auth', methods=['GET'])
# def hello_world():
#     user = request.args.get('q')
#     password = request.args.get('password')
#     print(f"USER: {user}  PASS: {password}")
#     response = {"success": 1}
#     return jsonify(response)


# if __name__ == "__main__":
#     app.run(debug=True,host='0.0.0.0', port=8080)




import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime, timedelta
from pymongo import ASCENDING,DESCENDING
load_dotenv()
# LOADING THE DATABASE
DB_URI = "mongodb+srv://devanshuagrawal99:Devanshu@oghbssw.rvaadkh.mongodb.net/?retryWrites=true&w=majority&appName=OGHBSSW"
client = MongoClient(DB_URI)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    print("Connected to MongoDB successfully!")
except ConnectionFailure as e:
    print("Could not connect to MongoDB: %s" % e)

db = client.OGHBSdatabase

#GETTING ALL THE COLLECTIONS

room_collection = db.room_collection
user_collection = db.user_collection
booking_collection = db.booking_collection

rooms = room_collection.find({}).sort("_id", DESCENDING)

for room in rooms: 
    print(room)




# import re
# def has_numbers(inputString):
#     return (not bool(re.search(r'\d', inputString)))

# print(has_numbers("I own 1 dog"))
# print(has_numbers("I own no dog"))
