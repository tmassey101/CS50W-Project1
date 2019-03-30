import os

from flask import Flask, session, jsonify, request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import json

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

gr_key = "lkPQBdBth7EI3WJjFYWawg"



#msin page, begin session if no existing user (or keep logged in as user)
@app.route("/", methods=["GET", "POST"])
def index():

    curUser = []
    
    if session.get("curUser") is None:
        session["curUser"] = []

        
    
    if request.method == "POST":
        
        submitUser = request.form.get("submitUser")
        curUser = submitUser

    return render_template("index.html", curUser=curUser)
    


#msin page, begin session if no existing user (or keep logged in as user)
#@app.route("/<string:name>")
#def userTest(name):

#    curUser = name
#    #return f"Hello, {name}!"
#    return render_template("index.html", curUser=curUser)




@app.route("/test")
def keytest():
        
    gr_key = "lkPQBdBth7EI3WJjFYWawg"

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": gr_key, "isbns": "9781632168146"})
    
    r = res.text

    print(r)
    print()
    print(res.headers)
    print()
    print(res.headers['Status'])
    print()
    #print(r.values)
    print(r[0])

    #parsed = json.loads(res.json())
    #print(parsed)
    
    #print(res.type)
    print(type(r))

    json_r = json.loads(r)

    #print(type(result))
    result = str(json_r['books'][0]['average_rating'])
    print("Book Avg:  "+ result)

    #result = result['id']

    return str(result)
