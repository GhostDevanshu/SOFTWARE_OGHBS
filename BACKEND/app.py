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
    curr_date = datetime.now()

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
    
def checkavailable():
    pass

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

# ROUTE TO CREATE A USER
@app.route('/register', methods=['POST'])
def register():

    reset_booking()

    if(isBlank(request.form['username']) or isBlank(request.form['roll_no']) or isBlank(request.form['first_name']) or isBlank(request.form['password']) or isBlank(request.form['address_line_1'])):
        return "300"
    if (user_collection.count_documents({"username": request.form['username']}) != 0):
        return "100"
    if (user_collection.count_documents({"roll_no": request.form['roll_no']}) != 0):
        return "200"
    if (has_numbers(request.form['first_name'] + " " + request.form['last_name'])):
        return "300"
    if (not request.form['age'].isdigit()):
        return "300"
    if (request.form['password'] != request.form['verify_password']):
        return "300"
    
    user = {
        'username': request.form['username'],
        'password': request.form['password'],
        'email': request.form['email'],
        'name': request.form['first_name'] + " " + request.form['last_name'],
        'roll_no': request.form['roll_no'],
        'age': request.form['age'],
        'gender': request.form['gender'],
        'address': str(request.form['address_line_1']) + ", "  + str(request.form['address_line_2']),
        'booking_ids': []
    }

    user_collection.insert_one(user)
    return "0"

@app.route('/login', methods=['POST'])
def login():
    reset_booking()

    if (isBlank(request.form["username"]) or isBlank(request.form["password"])):
        return "300"
    if (user_collection.count_documents({"username": request.form["username"]}) == 0):
        return "100"
    
    probable_user = user_collection.find_one({"username" : request.form["username"]})

    if (request.form["password"] != probable_user["password"]):
        return "200"
    else: 
        global cur_user
        cur_user = probable_user
        return "0"

@app.route('/logout',methods = ["GET"])
def logout():
    reset_booking()

    global cur_user
    cur_user = -1

    return "0"

@app.route('/available',methods = ["GET"])
def availability():
    reset_booking()
    global checkindate
    global checkoutdate
    checkindate = datetime(request.form['checkindate'])
    checkoutdate = datetime(request.form['checkoutdate'])

    response = checkavailable()
    
    pass

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


# START THE APP
if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0",port=5002)

