import os
from flask import Flask, request, session, redirect, \
	              url_for, render_template, flash, jsonify
	 
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker 
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash
from livereload import Server, shell
from models import db
from forms import RegistrationForm, LoginForm, SearchForm, ReviewForm
from services import getBookInfo

app = Flask(__name__)

# This section puts that app into development mode if ENV='dev'
# and production mode of ENV = prod
#ENV = 'dev'
ENV = 'prod'

if ENV == 'dev':
	app.debug = True
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testin123!@localhost/books'
	app.secret_key = 'removed for prod'
	engine = create_engine("postgresql://postgres:testin123!@localhost/books")
else:
	app.debug = False
	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
	app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
	engine = create_engine(os.environ.get('DATABASE_URL'))
	
# Only set this to true if you want notifications prior to and after changes
# are committed to the database.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db initilized and linked to app.
# Note 1: db object created in models.py
# Note 2: To set up a db, see dbtype_init.py files in books_dev folder
db.init_app(app)

# This prevents jsonify() from sorting dictionaries
app.config['JSON_SORT_KEYS'] = False

# sqlalchemy engine used to connect to existing database
sql_db = scoped_session(sessionmaker(bind=engine))

# Index Route: If user logged in, goes to profile, else goes to index.html
@app.route('/')
def index():
	if session.get('logged_in') == True:
		return redirect(url_for('profile'))
	else:	
		return render_template('index.html')
	
# Register Route: page for registering user, if successful goes to login.html
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm(request.form)
	
	if request.method == 'POST' and form.validate():
		username = form.username.data
		password = generate_password_hash(form.password.data)
		confirm = form.confirm.data
		password_match = check_password_hash(password, confirm)	
		
		print(password_match)
		user = sql_db.execute("SELECT * FROM users WHERE username = :username", {"username":username}).fetchall()
      
		if password_match == False:		
			return render_template('register.html', error='Passwords Do Not Match')
		else:
			if len(user) == 0:
				sql_db.execute("INSERT INTO users (username,  password) VALUES(:username, :password)", {"username": username, "password": password})
				sql_db.commit()
			else:
				return render_template('register.html', error='Username Already Exists')				
		flash('Registration Successful', 'success')
		return redirect(url_for('login'))
	else:
		return render_template('register.html')
		
	return render_template('register.html', form=form)

# Login Route: page for user login, if successful goes to profile.html
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	
	if request.method == 'POST':
		username = form.username.data
		password_candidate = form.password.data
		
		user = sql_db.execute("SELECT * FROM users WHERE username = :username", {"username":username}).fetchall()
		
		if len(user) != 0:
			#verify password
			password = user[0][2]
			result = check_password_hash(password, password_candidate)			
			if result == True:
				#create session
				session['logged_in'] = True
				session['username'] = username
				return redirect(url_for('profile'))
			else:				
				return render_template('login.html', error='Password Incorrect')			
		else:			
			return render_template('login.html', error='Username not found')
			
	return render_template('login.html')	

# Profile route: main profile page, books can be searched and past reviews can be viewed
@app.route('/profile', methods=['GET', 'POST'])
def profile():
	form = SearchForm(request.form)
	result = None
	titles = []
	authors = []
	scores = []
	reviews = []
	isbns = []
	
	# when user logs in, check db for all their reviews, 
	# and post them to the page through all_reviews variable
	review_query = sql_db.execute("Select * FROM reviews RIGHT JOIN books ON reviews.isbn = books.isbn WHERE username = :username", {"username": session['username']}  ).fetchall()
	print(review_query)
    
	for review in review_query:
		titles.append(review[7])
		authors.append(review[8])
		scores.append(review[1])
		reviews.append(review[2])
		isbns.append(review[4])

	if len(scores) == 0:
		all_reviews = 0
	else:
		all_reviews = zip(titles, authors, scores, reviews, isbns)
	
	# This section handles search queries (checks for isbn, title, or author) 	
	if request.method == 'POST':
		search = form.search.data
		
        # If first char entered is a number, then has to be isbn or typing error
		if search[0].isdigit():
			query = sql_db.execute("Select * From books WHERE isbn LIKE '%{0}%' LIMIT 25".format(search), {"search":search}).fetchall()
			if len(query) == 0:
				return render_template('profile.html', error='ISBN Not Found', all_reviews=all_reviews)
			else:
				return render_template('profile.html', result=query, all_reviews=all_reviews)		
		# Else if first char is text, convert search and db fields to lowercase 
		else:
			search = search.lower()
			query = sql_db.execute("Select * From books WHERE lower(author) LIKE '%{0}%' OR lower(title) LIKE '%{1}%' LIMIT 25".format(search, search), {"search":search}).fetchall()
			if len(query) == 0:
				return render_template('profile.html', error='No Match Found', all_reviews=all_reviews)
			else:
				return render_template('profile.html', result=query, all_reviews=all_reviews) 		
	return render_template('profile.html', result=result, all_reviews=all_reviews)

# Book route: when user selects a book after a search on their profile, book.html is returned
@app.route('/book/<string:isbn>', methods=['GET', 'POST'])
def book(isbn):
	form = ReviewForm(request.form)

	# Because an isbn check has already been performed in profile, no check is required
	query = sql_db.execute("Select * From books WHERE isbn = :isbn", {"isbn":isbn}).fetchall()
	
	# Grabs GoodReads review information using their API, gotBookInfo() is in services.py
	gr_data = getBookInfo(isbn, query)
	userReview =  sql_db.execute("SELECT * FROM reviews WHERE username = :username AND isbn = :isbn", {"username": session['username'], "isbn":isbn}).fetchall()
	allReviews =  sql_db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn":isbn}).fetchall()
	
	username = session['username']
	title = query[0][2]
	author = query[0][3]
	published = query[0][4]
	userscore = 0
	user_review = ''

	if len(userReview) > 0:
		userscore = userReview[0][1]
		user_review = userReview[0][2]
	else:
		if request.method == 'POST':
			userscore = form.score.data
			user_review = form.review.data
			sql_db.execute("INSERT INTO reviews (score, review, username, isbn) VALUES(:score, :review, :username, :isbn)", {"score": str(userscore), "review": user_review, "username": username, "isbn": isbn})
			sql_db.commit()
			
			# used for testing purposes only
			# print(isbn, username, userscore, user_review);
	
	return render_template('book.html', username = username, 
										isbn = isbn,
										title = title,
										author = author,
										published = published,
										userscore = userscore,
										user_review = user_review,
										gr_data = gr_data,
										allReviews=allReviews, 
										userReview=userReview)

# Logout route: logs out user and re-directs to login.html										
@app.route('/logout')
def logout():
	session.clear()
	flash('Logged Out', 'success')
	return redirect(url_for('login'))
	
# Simple api that allows access to book information using isbn numbers
# Test isbns: 055358202X (has reviews), 0307348245 (no reviews)
@app.route('/api/<isbn>')
def isbnAPI(isbn):
	if isbn[0].isdigit() and len(isbn) == 10:
		bookQuery = sql_db.execute("Select * From books WHERE isbn = :isbn", {"isbn":isbn}).fetchall()
		countQuery = sql_db.execute("Select COUNT(*) From reviews WHERE isbn = :isbn", {"isbn":isbn}).fetchall()
		avgReviewQuery = sql_db.execute("Select AVG(CAST(score AS int)) AS average_score From reviews WHERE isbn = :isbn", {"isbn":isbn}).fetchall()
		
		# used for testing purposes
		#print(countQuery[0][0])
		#print(avgReviewQuery[0][0])
		
		title = bookQuery[0][2]  
		author = bookQuery[0][3]
		year = bookQuery[0][4]
		review_count = countQuery[0][0]
		
		if len(bookQuery) == 0:
			return('No ISBN Match')
		elif review_count == 0:
			result = {
						"title"  : title,
						"author" : author,
						"year"   : year,
						"isbn"   : isbn	,
						"review_count" : 0,
						"avg_score" : "no reviews"
					}
			return jsonify(result)
		else:
			result = {
						"title"  : title,
						"author" : author,
						"year"   : year,
						"isbn"   : isbn,
						"review_count" : review_count,
						"avg_score" : str(round(avgReviewQuery[0][0], 2))
					}
			return jsonify(result)
	else:
		return 'ISBN Not Found'
		

def main():
	#server = Server(app.wsgi_app)
	#server.watch(os.path.join(os.getcwd(), 'static/*.css'))
	#server.watch(os.path.join(os.getcwd(), 'static/*.js'))
	#server.watch(os.path.join(os.getcwd(), 'templates/*.html'))
	#server.serve()
	
	# After developement finished, comment out secret key & server code 
	# and un-comment app.run()
	app.run()
	
if __name__ == '__main__':
	with app.app_context():
		main()
