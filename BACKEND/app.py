from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime, timedelta
import re
import copy
from bson import ObjectId
from pymongo import ASCENDING

app = Flask(__name__)
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
            if booking['booking_status'] == 'CONFIRMED':
                booking_collection.update_one(
                    {'_id': booking['_id']},  
                    {'$set': {'booking_status': 'COMPLETED'}}  
                )
            elif booking['booking_status'] == 'WAITLISTED':
                booking_collection.update_one(
                    {'_id': booking['_id']},  
                    {'$set': {'booking_status': 'COMPLETED','payment_status': 'REFUNDED'}}  
                )
            else:
                pass
        else:
            pass
    return
def checkavailable(guest_house):
    global checkindate
    global checkoutdate

    guest_house_detail = guest_house_collections.find_one({"code":guest_house})
    previous_bookings = guest_house_detail["prev_bookings"]

    for_each_room = guest_house_detail["rooms"]
    for add_days in range((checkoutdate - checkindate).days + 1):
        new_date = checkindate + timedelta(days=add_days)
        if (str(new_date.date()) in previous_bookings):
            for room in previous_bookings[str(new_date.date())].keys():
                if previous_bookings[str(new_date.date())][room] < for_each_room[room]: 
                    for_each_room[room] = previous_bookings[str(new_date.date())][room]
        else:
            continue
    
    data = {}
    data["rooms"] = []

    for room_code in guest_house_detail["rooms"].keys():
        room = room_collection.find_one({"code": room_code})

        data["rooms"].append(
            {
                "code" : room["code"],
                "description" : room["description"],
                "AC" : "YES" if room["AC"] else "NO",
                "floor" : room["floor"],
                "Occupancy": room["Occupancy"],
                "price_per_day": room["Price_per_day"],
                "available": for_each_room[room_code],
            }
        )
    return data
def checkavailablefordates(checkindate,checkoutdate,guest_house,room_code):
    guest_house_detail = guest_house_collections.find_one({"code":guest_house})
    previous_bookings = guest_house_detail["prev_bookings"]
    flag = 1
    for add_days in range((checkoutdate - checkindate).days + 1):
        new_date = checkindate + timedelta(days=add_days)
        if (str(new_date.date()) in previous_bookings):
            for room in previous_bookings[str(new_date.date())].keys():
                if room_code == room:
                    if previous_bookings[str(new_date.date())][room] <= 0:
                        flag=0
                        return flag
        else:
            continue
    return flag

def update_guest_house_booking(checkindate,checkoutdate,guest_house,room_code):
    guest_house_detail = guest_house_collections.find_one({"code":guest_house})

    previous_bookings = copy.deepcopy(guest_house_detail["prev_bookings"])
    for add_days in range((checkoutdate - checkindate).days + 1):
        new_date = checkindate + timedelta(days=add_days)
        if (str(new_date.date()) in previous_bookings):
            previous_bookings[str(new_date.date())][room_code] = previous_bookings[str(new_date.date())][room_code]-1
            pass
        else:
            previous_bookings[str(new_date.date())] = copy.deepcopy(guest_house_detail["rooms"])
            previous_bookings[str(new_date.date())][room_code] = previous_bookings[str(new_date.date())][room_code]-1
    print(previous_bookings)
    guest_house_collections.update_one({"code":guest_house},{"$set":{"prev_bookings":previous_bookings}})
    return

def construct_Booking_document():
    global curr_booking
    global cur_user
    booking_document = {
        "user_id" : str(user_collection.find_one({"username": cur_user["username"]})["_id"]),
        "checkindate": curr_booking["checkindate"],
        "checkoutdate": curr_booking["checkoutdate"],
        "payment_status": curr_booking["payment_status"],
        "cost": curr_booking["cost"],
        "individuals": curr_booking["individuals"],
        "booking_status": "CONFIRMED" if curr_booking["available"] > 0 else "WAITLISTED",
        "payment_details": curr_booking["payment_details"],
        "guest_house": curr_booking["guest_house"],
        "room_code": curr_booking["room_code"],
        "feedback": ""
    }

    update_guest_house_booking(datetime.strptime(curr_booking['checkindate'], "%Y-%m-%d"),datetime.strptime(curr_booking['checkoutdate'], "%Y-%m-%d"),curr_booking["guest_house"],curr_booking["room_code"])

    id_for_booking = str(booking_collection.insert_one(booking_document).inserted_id)

    cur_user["booking_ids"].append(id_for_booking)
    user_collection.update_one({"username":cur_user["username"]},{"$set":{"booking_ids":cur_user["booking_ids"]}})

    curr_booking = -1
    return

def initiatecurrbooking(form):
    global curr_booking
    print(curr_booking)
    print(form)
    curr_booking = {}

    curr_booking = {
        "checkindate" : form['checkindate'], 
        "checkoutdate" : form['checkoutdate'], 
        "guest_house" : form["guest_house"],
        "room_code" : form["room_code"],
        "occupancy" : int(form["occupancy"]),
        "available" : int(form["available"])
    }

    print(curr_booking)
    data = {
        "occupancy" : form["occupancy"]
    }

    return data

def addindividualstocurr(form):
    global curr_booking
    print(curr_booking)
    individuals_list = []

    cost_of_food = 0
    for i in range(0, curr_booking["occupancy"]):
        individual = {}
        if(isBlank(form[f"peopleInfo[{i}][name]"]) or isBlank(form[f"peopleInfo[{i}][age]"]) or isBlank(form[f"peopleInfo[{i}][gender]"]) or isBlank(form[f"peopleInfo[{i}][relation]"]) or isBlank(form[f"peopleInfo[{i}][food]"])):
            response = {
                "status" : 300,
                "message" : "A Field is empty",
                "data" : {}
            }
            return jsonify(response)
        
        individual = {
            "name" : form[f"peopleInfo[{i}][name]"],
            "age" : form[f"peopleInfo[{i}][age]"],
            "gender" : form[f"peopleInfo[{i}][gender]"],
            "relation" : form[f"peopleInfo[{i}][relation]"],
            "food_option": form[f"peopleInfo[{i}][food]"]
        }    
        individuals_list.append(individual)
        cost_of_food += (0.2 * food_options.find_one({"description": form[f"peopleInfo[{i}][food]"]})["Price"])

    curr_booking["individuals"] = individuals_list

    room = room_collection.find_one({"code": curr_booking["room_code"]})
    total_cost = 0.2 * ((  room["Price_per_day"] ) + cost_of_food) * (int((datetime.strptime(curr_booking['checkoutdate'], "%Y-%m-%d") - (datetime.strptime(curr_booking['checkindate'], "%Y-%m-%d"))).days) + 1)
    curr_booking["cost"] = total_cost
    data = {
        "price" : total_cost
    }
    print(curr_booking)
    response = {
        "status": 0,
        "message": "added individuals",
        "data": {}
    }
    return response

def payment_completion(form):
    global curr_booking
    if (False):
        response = {
            "status" : 300,
            "message" : "Card Details are incorrect",
            "data": {}
        }
        return jsonify(response)

    card_details = {
        "card_number" : form["card_number"],
        "card_expiry" : form["expiry_month"],
        "card_cvv" : form["cvv"],
        "name_on_card" : form["name_on_card"]
    }

    curr_booking["payment_details"] = card_details
    curr_booking["payment_status"] = "COMPLETED"
    print(curr_booking)
    construct_Booking_document()
    data = {}
    return data

def cancel_booking(booking_id):
    booking = booking_collection.find_one({"_id":ObjectId(booking_id)})
    print(booking)
    if booking["booking_status"] != "CONFIRMED" and booking["booking_status"] != "WAITLISTED":
        data = {}
        print("working")
        return (data)
    booking_collection.update_one({"_id":ObjectId(booking_id)},{"$set": {"booking_status":"CANCELLED"}})
    booking_collection.update_one({"_id":ObjectId(booking_id)},{"$set": {"payment_status":"REFUNDED"}})
    checkindate = datetime.strptime(booking['checkindate'], "%Y-%m-%d")
    checkoutdate = datetime.strptime(booking['checkoutdate'], "%Y-%m-%d")

    guest_house_detail = guest_house_collections.find_one({"code":booking["guest_house"]})


    ### update data base guest 
    previous_bookings = copy.deepcopy(guest_house_detail["prev_bookings"])
    for add_days in range((checkoutdate - checkindate).days + 1):
        new_date = checkindate + timedelta(days=add_days)
        if (str(new_date.date()) in previous_bookings):
            previous_bookings[str(new_date.date())][booking["room_code"]] = previous_bookings[str(new_date.date())][booking["room_code"]]+1
            pass
        else:
            previous_bookings[str(new_date.date())] = copy.deepcopy(guest_house_detail["rooms"])
            previous_bookings[str(new_date.date())][booking["room_code"]] = previous_bookings[str(new_date.date())][booking["room_code"]]+1
    print(previous_bookings)
    guest_house_collections.update_one({"code":booking["guest_house"]},{"$set":{"prev_bookings":previous_bookings}})

    ### update data base booking
    smaller_booking_users = booking_collection.find({"guest_house":booking["guest_house"],"room_code":booking["room_code"],"booking_status":"WAITLISTED"}).sort("_id", ASCENDING)
    print("********************")
    print(smaller_booking_users)
    print("********************")
    for booking_loop in smaller_booking_users:
        print("11111111111111")
        print(booking_loop)
        print("11111111111111")
        flag = checkavailablefordates(datetime.strptime(booking_loop['checkindate'], "%Y-%m-%d"),datetime.strptime(booking_loop['checkindate'], "%Y-%m-%d"),booking_loop["guest_house"],booking_loop["room_code"])
        if flag == 1:
            booking_collection.update_one({"_id":booking_loop["_id"]},{"$set":{"booking_status":"CONFIRMED"}})
            break
    
    data = {}
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
        'verified': "NOT VERIFIED",
        'address': str(request.form['address_line_1']) + ", "  + str(request.form['address_line_2']),
        'booking_ids': []
    }

    ########inserting the documnet into the database##############
    user_collection.insert_one(user)
    user["_id"] = str(user["_id"])
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
        if (probable_user["username"]=="admin"):
            response = {
                "status":1000,
                "message": "login successful",
                "data": {}
            }
            return jsonify(response)

        cur_user = copy.deepcopy(probable_user)
        response = {
            "status":0,
            "message": "login successful",
            "data": probable_user
        }
        print(probable_user)
        return jsonify(response)

############ LOGOUT ROUTE ############
######################################
@app.route('/logout',methods = ["GET"])
def logout():
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
    global checkindate
    global checkoutdate
    checkindate = datetime.strptime(request.form['checkindate'], "%Y-%m-%d")
    checkoutdate = datetime.strptime(request.form['checkoutdate'], "%Y-%m-%d")
    message = "Showing availability between the provided checkin and checkout dates"

    if (checkindate.date() < datetime.now().date()):
        checkindate = datetime.strptime(str(datetime.now().date()), "%Y-%m-%d")
        message = "Check-in date is in the past showing availability from now to Checkout"

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
            "message": message,
            "data": {}
        }
        return jsonify(response)

    data = checkavailable(guest_house=str(request.form["guest_house"]))

    response = {
        "status" : 0,
        "message" : "Bookings for each day fetched properly",
        "data" : data
    }

    return jsonify(response)

@app.route('/initiatebooking',methods=["POST"])
def initiatebooking():
    if (cur_user["verified"] != "VERIFIED"):
        response = {
            "status": 100,
            "message": "USER IS NOT VERIFIED BY ADMIN",
            "data": {}
        }
        return jsonify(response)
    response =  initiatecurrbooking(request.form)

    return jsonify(response)

@app.route('/addingindividual', methods = ["POST"])
def addindividuals():
    response = addindividualstocurr(request.form)
    return jsonify(response)

@app.route('/payment_done',methods = ["POST"])
def payment_done():
    reponse =  payment_completion(request.form)
    return jsonify(reponse)

@app.route('/cancellation',methods=["POST"])
def cancellation():
    print(request.form)
    response = {
        "status" : 0,
        "message" : "Cancelled Booking",
        "data": cancel_booking(request.form["booking_id"])
    }
    return jsonify(response)

@app.route('/profile',methods=["GET"])
def get_profile():
    global cur_user
    if (cur_user == -1):
        response = {
            "status": 100,
            "message": "No user is logged in",
            "data": {}
        }
        return jsonify(response)
    else:
        list_of_ids = cur_user["booking_ids"]
        cur_user["bookings"] = []
        for booking_id in list_of_ids:
            booking = booking_collection.find_one({"_id":ObjectId(booking_id)})
            booking["_id"] = str(booking["_id"])
            cur_user["bookings"].append(copy.deepcopy(booking))
        response = {
            "status": 0,
            "message": "fetched user details",
            "data": cur_user
        }
        return jsonify(response)

@app.route('/getoccupancy',methods=["GET"])
def get_occupancy():
    global curr_booking
    response = {
        "status": 0,
        "message": "fetched successfully",
        "data": {
            "occupancy":curr_booking["occupancy"]
        }
    }
    return jsonify(response)

@app.route('/get_payment', methods = ["GET"])
def get_payment():
    global curr_booking
    response = {
        "status": 0,
        "message": "Got the price for stay",
        "data":{
            "cost": curr_booking["cost"]
        }
    }
    return jsonify(response)

@app.route('/feedback',methods=["POST"])
def set_feedback():
    booking_collection.update_one({"_id": ObjectId(request.form["booking_id"])},{"$set":{"feedback":request.form["feedback"]}})
    response = {
        "status": 0,
        "message": "Feedback set successfully",
        "data": {}
    }
    return jsonify(response)

#### admin features
@app.route('/get_all_users', methods=["GET"])
def get_all_users():
    
    if (user_collection.count_documents({}) == 0):
        response = {
            "status": 100,
            "message": "User Already Kicked Out",
            "data": {}
        }
        return jsonify(response)
    data = []
    for user in user_collection.find({"username": {"$ne": "admin"}}):
        user["_id"] = str(user["_id"])
        data.append(user)

    response = {
        "status": 0,
        "message": "GOT all users",
        "data": data
    }
    return jsonify(response)

@app.route('/get_all_bookings', methods=["GET"])
def get_all_bookings():
    print(request.form)
    if (booking_collection.count_documents({}) == 0):
        response = {
            "status": 100,
            "message": "Booking collection is empty",
            "data": {}
        }
        return jsonify(response)
    data = []
    for booking in booking_collection.find({}):
        booking["_id"] = str(booking["_id"])
        data.append(booking)

    response = {
        "status": 0,
        "message": "GOT all users",
        "data": data
    }
    return jsonify(response)

@app.route('/kick_user',methods= ["POST"])
def kick_user():

    if (user_collection.count_documents({"_id":ObjectId(request.form["user_id"])})==0):
        response = {
            "status": 100,
            "message": "User Already Kicked Out",
            "data": {}
        }
        return jsonify(response)
    

    user_id = request.form["user_id"]
    for user in user_collection.find({"_id": ObjectId(user_id)}):
        for booking_id in user["booking_ids"]:
            cancel_booking(booking_id)

    user_collection.delete_one({"_id": ObjectId(user_id)})
    response = {
        "status": 0,
        "message": f"KICKED OUT USER {user_id}",
        "data": {}
    }

    return jsonify(response)

@app.route('/verify_user',methods = ["POST"])
def verify_user():
    print("********************")
    print(request.form)
    print("********************")
    if (user_collection.count_documents({"_id":ObjectId(request.form["user_id"])})==0):
        response = {
            "status": 100,
            "message": "Internal Server Error",
            "data": {}
        }
        return jsonify(response)
    
    user_id = request.form["user_id"]

    user_collection.update_one({"_id":ObjectId(user_id)},{"$set":{"verified": "VERIFIED"}})
    response = {
        "status": 0,
        "message": "User verified",
        "data": {}
    }

    return jsonify(response)

# START THE APP
if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0",port=5002)

