import os
from flask import Flask, session, jsonify, request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import json
import csv


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


#import data in main function

def main():
    file = open("books.csv")
    reader = csv.reader(file)
    
    for row in file:
        for isbn, title, author, year in reader:

            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                        {"isbn": isbn, "title": title, "author": author, "year": year})
            print(f"Addeding book: {isbn}, -   {title}.")
        db.commit()
        
    print(f"Upload complete")

if __name__ == "__main__":
    main()
