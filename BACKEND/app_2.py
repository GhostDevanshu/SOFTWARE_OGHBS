from flask import Flask, request, redirect, url_for, render_template
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

# GLOBAL AVRIABLES 

cur_user = -1



#HELPER FUNCTIONS
def has_numbers(inputString):
    return (bool(re.search(r'\d', inputString)))

def isBlank (myString):
    print(myString)
    print(not (myString and myString.strip()))
    return not (myString and myString.strip())


#verifier
# print("WORKING")

#ROUTE FOR CHECKING
@app.after_request
def add_cors_headers(response):
    global cur_user
    print(cur_user)
    return response

# ROUTE TO CREATE A USER
@app.route('/register', methods=['POST'])
def register():
    print("WORKING")
    if(isBlank(request.form['username']) or isBlank(request.form['roll_no']) or isBlank(request.form['first_name']) or isBlank(request.form['password']) or isBlank(request.form['address line 1'])):
        #return render_template('register.html',status_code = 300)
        return "300"
    username = request.form['username']
    roll_no = request.form['roll_no']
    if (user_collection.count_documents({"username": username}) != 0):
        #return render_template('register.html',status_code = 100)
        return "100"
    if (user_collection.count_documents({"roll_no": roll_no}) != 0):
        #return render_template('register.html',status_code = 200)
        return "200"

    name = request.form['first_name'] + " " + request.form['last_name']

    if (has_numbers(name)):
        #return render_template('login.html',status_code = 300)
        return "300"
    if (not request.form['age'].isdigit()):
        #return render_template('login.html',status_code = 300)
        return "300"
    if (request.form['password'] != request.form['verify password']):
        #return render_template('login.html',status_code = 300)
        return "300"
    password = request.form['password']
    user = {
        'username': username,
        'password': password,
        'name': name,
        'roll_no': roll_no,
        'age': request.form['age'],
        'gender': request.form['gender'],
        'address': str(request.form['address line 1']) + ", " +str(request.form['address line 2']),
        'booking_ids': []
    }
    user_collection.insert_one(user)
    return "0"

@app.route('/login', methods=['POST'])
def login():
    #if request.method == 'GET':
    username = request.form["username"]
    password = request.form["password"]
    print(username)
    print(password)
    if (user_collection.count_documents({"username": username}) == 0):
        #return render_template('login.html',status_code = 100)
        return "100"
    probable_user = user_collection.find_one({"username" : username})
    if (password != probable_user["password"]):
        #return render_template('profile.html',status_code = 200)
        return "200"
    else: 
        global cur_user
        cur_user = probable_user
        # return redirect(url_for('profile', userid = probable_user["_id"]))
        return "0"

@app.route('/logout',methods = ["GET"])
def logout():
    global cur_user
    cur_user = -1
    #return render_template('index.html')
    return "0"

# START THE APP
if __name__ == '__main__':
    app.run(debug=True, port=5002)

