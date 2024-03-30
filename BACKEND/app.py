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

# CHECK THE DATABASE IF IT IS CONNECTED
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
guest_house_collections = db.guest_house_collection
food_options = db.food_options

# GLOBAL VAVRIABLES 

cur_user = -1
checkindate = datetime.now()
checkoutdate = datetime.now()
curr_booking = -1

#HELPER FUNCTIONS
def has_numbers(inputString):
    return (bool(re.search(r'\d', inputString)))
def isBlank (myString):
    return not (myString and myString.strip())

def update_system():
    bookings = booking_collection.find()
    
    for booking in bookings:
        if  datetime.strptime(booking["checkindate"], "%Y-%m-%d").date() < datetime.now().date():
            if booking['confirmation_status'] == 'confirmed':
                booking_collection.update_one(
                    {'_id': booking['_id']},  
                    {'$set': {'confirmation_status': 'completed'}}  
                )
            elif booking['confirmation_status'] == 'waitlist':
                booking_collection.update_one(
                    {'_id': booking['_id']},  
                    {'$set': {'confirmation_status': 'completed','payment_status': 'refunded'}}  
                )
            else:
                pass
        else:
            pass
    return

def reset_booking():
    global curr_booking
    curr_booking = -1
    
def checkavailable(guest_house):
    global checkindate
    global checkoutdate

    guest_house_detail = guest_house_collections.find_one({"code":guest_house})
    previous_bookings = guest_house_detail["prev_bookings"]

    for_each_date = {}
    for add_days in range((checkoutdate - checkindate).days + 1):
        new_date = checkindate + timedelta(days=add_days)
        
        if (str(new_date.date()) in previous_bookings):
            for_each_date[str(new_date.date())] = previous_bookings[str(new_date.date())]
        else:
            for_each_date[str(new_date.date())] = guest_house_detail["rooms"]
    
    data = {}
    data["rooms"] = []

    for room_code in guest_house_detail["rooms"].keys():
        room = room_collection.find_one({"code": room_code})

        data["rooms"].append(
            {
                "code" : room["code"],
                "description" : room["description"],
                "AC" : room["AC"],
                "floor" : room["floor"],
                "Occupancy": room["Occupancy"],
                "price_per_day": room["Price_per_day"]
            }
        )
    
    data["available_each_date"] = for_each_date

    return data

#ROUTE FOR CHECKING
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    update_system()

    return response

@app.route('/', methods= ["POST","GET"])
def hello_world():
    print("HELLO WORLD")
    return "0"

###########################
# ROUTE TO CREATE A USER
@app.route('/register', methods=['POST'])
def register():
    ########################
    reset_booking()
    print(request.form)
    ######## CHECKS #########
    if(isBlank(request.form['username']) or isBlank(request.form['roll_no']) or isBlank(request.form['first_name']) or isBlank(request.form['password']) or isBlank(request.form['address_line_1'])):
        response = {
            "status":300,
            "message": "Blank field has been provided",
            "data": {}
        }
        return jsonify(response)
    
    if (user_collection.count_documents({"username": request.form['username']}) != 0):
        response = {
            "status":100,
            "message": "Username Already Exists",
            "data": {}
        }
        return jsonify(response)
    if (user_collection.count_documents({"roll_no": request.form['roll_no']}) != 0):
        response = {
            "status":200,
            "message": "Roll no. is already linked to a different user",
            "data": {}
        }
        return jsonify(response)
    if (has_numbers(request.form['first_name'] + " " + request.form['last_name'])):
        response = {
            "status":300,
            "message": "Name cannot have digits in it",
            "data": {}
        }
        return jsonify(response)
    if (not request.form['age'].isdigit()):
        response = {
            "status":300,
            "message": "Age has to be a number",
            "data": {}
        }
        return jsonify(response)
    if (request.form['password'] != request.form['verify_password']):
        response = {
            "status":300,
            "message": "Password Verification failed",
            "data": {}
        }
    
    ######### creating ###########
    user = {
        'username': request.form['username'],
        'password': request.form['password'],
        'email': request.form['email'],
        'name': request.form['first_name'] + " " + request.form['last_name'],
        'roll_no': request.form['roll_no'],
        'age': int(request.form['age']),
        'gender': request.form['gender'],
        'address': str(request.form['address_line_1']) + ", "  + str(request.form['address_line_2']),
        'booking_ids': []
    }
    user_collection.insert_one(user)

    response = {
            "status":0,
            "message": "User created succesfully",
            "data": user
        }

    return jsonify(response)

## LOGIN ENDPOINT
####################

@app.route('/login', methods=['POST'])
def login():
    ##########################
    reset_booking()
    print(request.form)
    ############### CHECKS ###############
    if (isBlank(request.form["username"]) or isBlank(request.form["password"])):
        response = {
            "status":300,
            "message": "A Field is blank",
            "data": {}
        }
        return jsonify(response)
    if (user_collection.count_documents({"username": request.form["username"]}) == 0):
        response = {
            "status":100,
            "message": "User doesn't Exist",
            "data": {}
        }
        return jsonify(response)
    
    ################# PASSWORD VERIFICATION ###################
    probable_user = user_collection.find_one({"username" : request.form["username"]})
    probable_user['_id'] = str(probable_user['_id'])
    if (request.form["password"] != probable_user["password"]):
        response = {
            "status":200,
            "message": "Incorrect Password",
            "data": {}
        }
        return jsonify(response)
    else: 
        global cur_user
        cur_user = probable_user
        response = {
            "status":0,
            "message": "login successful",
            "data": probable_user
        }
        return jsonify(response)

############ LOGOUT ROUTE ############
######################################
@app.route('/logout',methods = ["GET"])
def logout():
    ########################
    reset_booking()

    ####### SET THE CURRENT USER TO -1
    global cur_user
    cur_user = -1

    response = {
            "status":0,
            "message": "Logout Successful",
            "data": {}
        }
    return "0"


####### checking availability route

@app.route('/checkavailable',methods = ["POST"])
def availability():
    print("routed")
    reset_booking()
    global checkindate
    global checkoutdate
    checkindate = datetime.strptime(request.form['checkindate'], "%Y-%m-%d")
    checkoutdate = datetime.strptime(request.form['checkoutdate'], "%Y-%m-%d")
    print(checkindate)
    print(checkoutdate)
    if (checkindate.date() < datetime.now().date()):
        checkindate = datetime.strptime(str(datetime.now().date()), "%Y-%m-%d")

    if (checkindate.date() < datetime.now().date() or checkoutdate.date() < datetime.now().date()):
        response = {
            "status":300,
            "message": "Provided dates are in the past",
            "data":{} 
        }
        return jsonify(response)

    if (checkoutdate.date() < checkindate.date()):
        response = {
            "status":300,
            "message": "check-out date is before check-in date. REVERSE TIME ERROR",
            "data": {}
        }

    data = checkavailable(guest_house=str(request.form["guest_house"]))

    response = {
        "status" : 0,
        "message" : "Bookings for each day fetched properly",
        "data" : data
    }

    return jsonify(response)

@app.route('/book',methods= ["POST"])
def book():
    pass

@app.route('/payement_done',methods = ["POST"])
def payment_done():
    pass

@app.route('/cancellation',methods=["POST"])
def cancellation():
    reset_booking()
    pass

@app.route('/profile',methods=["GET"])
def get_profile():
    global cur_user
    print(cur_user)
    if (cur_user == -1):
        response = {
            "status": 100,
            "message": "No user is logged in",
            "data": {}
        }
        return jsonify(response)
    else:
        response = {
            "status": 0,
            "message": "fetched user details",
            "data": cur_user
        }
        return jsonify(response)


# START THE APP
if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0",port=5002)

