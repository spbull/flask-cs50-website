import os
import csv
from models import *

print(os.environ.get('DATABASE_URL'))
print(os.environ.get('SECRET_KEY'))

# This file is used to populate db's on heroku.
# It allows for database table creation (db.create_all()) 
# and also populates the books table with data from an external CSV file

# After db is created in heroku app and all files uploaded from github
# go to more tab on top-right of heroku, click on run console, then
# type: python script-name.py to run

print('testing pos DAMMMIIIIIIIIIIIIT')

#note db variable is created in models
def loadCSV():
	f = open("books.csv")
	reader = csv.reader(f)
	for isbn, title, author, year in reader:
		db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title , :author ,:year)", {"isbn":isbn, "title":title, "author":author, "year":year})
		print(f"Added book to db: title:{title}, author:{author}, year:{year}, isbn:{isbn}")
	db.commit()
	
#db.create_all()
#loadCSV()
	

