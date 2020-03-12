# This file is used to populate db's on heroku.
# It allows for database table creation (db.create_all()) 
# and also populates the books table with data from an external CSV file

# After db is created in heroku app and all files uploaded from github
# go to more tab on top-right of heroku, click on run console, then
# type: python script-name.py to run

import os
import csv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker 
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
engine = create_engine(os.environ.get('DATABASE_URL'))
 
#note db variable is created in models
def loadCSV():
	db = scoped_session(sessionmaker(bind=engine))
	f = open("books.csv")
	reader = csv.reader(f)
	for isbn, title, author, year in reader:
		db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title , :author ,:year)", {"isbn":isbn, "title":title, "author":author, "year":year})
		print(f"Added book to db: title:{title}, author:{author}, year:{year}, isbn:{isbn}")
	db.commit()

def main():
	print('Creating Tables')
	db.create_all()
	
	print('Populating books table')
	loadCSV()
	
if __name__ == '__main__':
	with app.app_context():
		main()
