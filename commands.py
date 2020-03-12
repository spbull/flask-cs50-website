import click
from flask.cli import with_appcontext
from models import *

def loadCSV():
	f = open("books.csv")
	reader = csv.reader(f)
	for isbn, title, author, year in reader:
		testdb.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title , :author ,:year)", {"isbn":isbn, "title":title, "author":author, "year":year})
		print(f"Added book to db: title:{title}, author:{author}, year:{year}, isbn:{isbn}")
	testdb.commit()
	
# This is used for deployement on heroku specifically.
# it allows for database table creation and to populate the books table
# on heroku after db is created and all files uploaded from github
# go to more tab on top-right of heroku, click on run console, then
# type: flask create_tables to run and db should then be set up
@click.command(name='create_tables')
@with_appcontext
def create_tables():
	db.create()
	loadCSV()
	

