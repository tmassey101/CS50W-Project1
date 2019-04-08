import os

from flask import Flask, session, jsonify, request, render_template
from flask_session import Session
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import json
from json import dumps

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
@app.route("/search", methods=["POST"])
def search():

    searchText = []
    
    #if request.method == "POST":
    searchText = request.form.get("searchText")
    searchString = "%" + searchText + "%"
    
    query = db.execute("SELECT isbn,title,author,year FROM books WHERE isbn LIKE :searchText OR title LIKE :searchText OR author LIKE :searchText LIMIT 20",{"searchText": searchString}).fetchall()
    
    for book in query:
        print(book)

    return render_template("results.html", query=query)
    
    

    
@app.route("/api/<string:isbn>", methods = ["GET"])
def isbn(isbn):

    result = []

    isbnsearch = str(isbn)
    
    books = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn" : isbnsearch}).fetchone()
    
    print(books)

    id = books[0]
    isbn = books[1]
    title = books[2]
    author = books[3]
    year = books[4]

    #print("title:", title)
    grresult = goodreadsapi(isbn)

    average_score = grresult['average_rating']
    review_count = grresult['reviews_count']

    result =  json.dumps({"title": title, "author": author, "year": year, "isbn": isbn, "review_count": review_count, "average_score": average_score})
    
    return result

def goodreadsapi(isbn):
        
    gr_key = "lkPQBdBth7EI3WJjFYWawg"

    results = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": gr_key, "isbns": "9781632168146"})
    
    results = results.json()
    results = results['books']
    
    for result in results:
        response = {'average_rating': result['average_rating'], "reviews_count": result['reviews_count']}

    return response

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
    result = json_r['books'][0]

    #result = result['id']

    return str(result)

if __name__ == '__main__':
   app.run(debug = True)