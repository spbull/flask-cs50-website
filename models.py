from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#db tables schema
class Books(db.Model):
	__tablename__ = "books"
	id = db.Column(db.Integer, primary_key = True)
	isbn = db.Column(db.String(100), nullable = False, unique=True)
	title = db.Column(db.String(100), nullable = False)
	author = db.Column(db.String(100), nullable = False)
	year = db.Column(db.String(100), nullable = False)
	
class Users(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(30), nullable = False, unique=True)
	password = db.Column(db.String(100), nullable = False)

class Reviews(db.Model):
	__tablename__ = "reviews"
	id = db.Column(db.Integer, primary_key = True)
	score = db.Column(db.String(2), nullable = True)
	review = db.Column(db.String(195), nullable = True)	
	username = db.Column(db.String(50), nullable = False)
	isbn = db.Column(db.String(10), db.ForeignKey("books.isbn"), nullable=False)