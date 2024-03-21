from flask import Flask,  jsonify, request
import os
from dotenv import load_dotenv
import pickle
from datetime import datetime, timedelta

app = Flask(__name__)

# MAIN PART
try:
    # OPEN AND LOAD DATABASE FILE
    with open('database.pkl', 'rb') as file:
        database = {}
        database = pickle.load(file)

except FileNotFoundError:
    # FILE NOT EXIST
    print("File not found. Creating a new empty list.")
    database = {}

#DEFINING GLOABL VARIABLES TO BE USED FOR PROCESSING DURING RUNTIME
curUserId = -1
checkInDate = datetime.now()
checkOutDate = datetime.now()
srt = '0'
foodId = '0'
availableOnly = '0'
roomId = 0

#CLASSES TO BE DEFINED
class user:
    def __init__(self,id,username,password,first_name,last_name,address_line_1,address_line_2,):
        self.id = id
        self.username = username
        self.password = password
        self.name = first_name + " " + last_name
        self.address = address_line_1 + ", " + address_line_2

        

class room:
    pass
class Food_option:
    pass
class Booking_instance:
    pass
class Auth_instance:
    pass

class data:
    def __init__(self,database):
        self.users = {}
        self.rooms = {}
        self.bookings = {}
        self.food_options = {}
        self.set_database(database=database)
    
    def set_database(self,database):
        self.users = database["USERS"]
        self.rooms = database["ROOMS"]
        self.bookings = database["BOOKINGS"]
        self.food_options = database["FOOD"]


try:
    with open('database.pkl', 'rb') as file:
        database = pickle.load(file)
except:
    database = data()




@app.after_request
def add_cors_headers(response):
    global database
    with open("database.pkl", 'wb') as file:  #UPDATE THE BACKEND DATABASE
            pickle.dump(database,file) 



    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/', methods=['GET'])
def hello_world():
    response = {}
    response["error"] = None
    response["results"] = {}
    return response





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

