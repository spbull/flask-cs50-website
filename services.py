import requests
import pprint
import bs4
import re

# Grabs book review and ratings info from goodreads.com
def getBookInfo(isbn, query):
	key = '6qn1mohBV7z7eebcE7mjQ'
	secret = 'cy4NdOGAVPvsPWmIdqhjxZ2thdkGxSqdJLXVf22HFLQ'
	title = query[0][2] 
	author = query[0][3]
	
	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": isbn})

	return res.json()