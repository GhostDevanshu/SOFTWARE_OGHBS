from flask import Flask,  jsonify, request
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime, timedelta


# MAKING THE CONNECTION
load_dotenv()
app = Flask(__name__)

DB_URI = os.getenv('DB_URI')
client = MongoClient(DB_URI)
db = client.OGHBSdatabase

#GETTING ALL THE DATABASE
user = db.user_database
food_options = db.food_options


#CHECKING THE CONNECTION
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    print("Connected to MongoDB successfully!")
except ConnectionFailure as e:
    print("Could not connect to MongoDB: %s" % e)

#DEFINING GLOABL VARIABLES TO BE USED FOR PROCESSING DURING RUNTIME
curUserId = -1
checkInDate = datetime.now()
checkOutDate = datetime.now()
srt = '0'
foodId = '0'
availableOnly = '0'
roomId = 0

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/sign_up', methods=['POST'])
def sign_up_user():
    status_code = 0


    return status_code





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

