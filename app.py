# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask,redirect
from flask import render_template
from flask import request,session,url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# -- Initialization section --
app = Flask(__name__)

events = [
    {"event": "First Day  Classes", "date": "2019-08-21"},
    {"event": "Winter Break", "date": "2019-12-20"},
    {"event": "Finals Begin", "date": "2019-12-01"}
]

app.secret_key = 'LeveneTeam'
# name of database
app.config['MONGO_DBNAME'] = 'database'

# URI of database

mongo = PyMongo(app)

# -- Routes section --
# INDEX


@app.route('/')
@app.route('/index')
def index():

    #connect to db

    collection = mongo.db.events

    #find all data

    events = collection.find({})

    #return a message
    return render_template('index.html', events=events)


# CONNECT TO DB, ADD DATA

@app.route('/add')
def add():
    # connect to the database
    events = mongo.db.events
    # insert new data
    events.insert({"event": "Graduate", "date": "06-02-16"})
    # return a message to the user
    return "Finna b lit"

# #user to add new event


@app.route('/events/new', methods=['GET', 'POST'])
def new_event():
    if request.method == "GET":
        return render_template("new_event.html")
    else:
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        user_name = request.form['user_name']
#connect to db
        collection = mongo.db.events
#insert new data
        collection.insert({"event": event_name, "date": event_date, "user": user_name})
#return a message to the user
        return redirect('/')


#show only the individual users events
@app.route('/name/<name>')
def name(name):
    collection = mongo.db.events
    # name = session['username']
    events=collection.find({"user":name})
    return render_template('person.html',events=events)


# user to add new event

# @app.route('/events/new', methods=['GET','POST'])

# def new_event():
#     if request.method == "GET":
#         return render_template("new_event.html")
#     else:
#         return "data added"

@app.route('/event/<eventID>')

def event(eventID):
    #connect to db
    collection = mongo.db.events
    #find all data
    event = collection.find_one({"_id":ObjectId(eventID)})
    
    #return a message
    return render_template('event.html',event = event)


#sign up for web

@app.route('/signup', methods=['POST','GET'])

def signup():
    if request.method == "POST":
        users = mongo.db.users
        exisiting_user = users.find_one({'name':request.form['username']})

        if exisiting_user is None:
            users.insert({'name': request.form['username'],'password': request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return "That user name is already in use"

    return render_template('/signup.html')

#Login
@app.route('/login',methods=['POST'])

def login():
    users = mongo.db.users
    login_user =users.find_one({'name': request.form['username']})

    if login_user:
        if request.form['password'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return "Invalid username password combination"


#logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#show only my events?
@app.route('/myevents')
def myevents():
    collection = mongo.db.events
    name = session['username']
    events=collection.find({"user":name})
    return render_template('person.html',events=events)