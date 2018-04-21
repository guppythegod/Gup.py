from __future__ import print_function
from flask import Flask, redirect, render_template, request, json
import sqlite3
import os
import random
import sys

""" 
KEY
0 = unknown error, unsuccessful
1 = successful operation
2 = IntegrityError, unsuccessful

-- url_data --
| unique_id | url | clicks | 

RESOURCES: https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972

"""
# --- SET UP --- #

app = Flask(__name__)
sqlite_file = "url_db.sqlite"
table = "url_data"
cwd = os.path.dirname(os.path.realpath(__file__))

conn = sqlite3.connect(cwd + "/" + sqlite_file)
c = conn.cursor()

# --- MODULES --- #

"""Return the whole database and its values, all printed nice and neat -- for debugging and development"""

def read_url_data():
	try:
		c.execute("""SELECT * FROM url_data;""")
	except Exception as e:
		print(e)
	results = c.fetchall()
	print("| unique_id | url | clicks |")
	for i in range(len(results)):
		print(results[i])

"""Deletes everything from the url_data table -- for debugging and development"""

def delete_url_data():
	c.execute("""DELETE FROM url_data;""")
	conn.commit()

""" Gets the url thats mapped to a a specific unique_id from the sqlite database """

def get_url(unique_id):
	conn = sqlite3.connect(cwd + "/" + sqlite_file)
	c = conn.cursor()
	try:
		c.execute("""SELECT url FROM url_data WHERE unique_id = ?;""", [unique_id]) # gets the url from the unique_id
		return str(c.fetchall()[0][0]) # returns back that the query retrieved from the db as a str (just incase)
	except Exception as e: # Unknown error
		return 0 # operation was unsuccessful so send back exit_code=0
  
""" Generates a unique_id for a url, that is no present in the database """

def generate_unique_id():
	conn = sqlite3.connect(cwd + "/" + sqlite_file)
	c = conn.cursor()
	unique_id = ""
	for i in range(4):
		unique_id += str(random.randint(0, 9))
	if not c.execute("""SELECT url FROM url_data WHERE unique_id = ?""", [unique_id]).fetchall():
		return unique_id
	else:
		generate_unique_id()

""" Creates a new mapping in the database with a unique_id and a url """

def create_url_mapping(unique_id, url):
	print(unique_id, file=sys.stderr) # debugger
	print(url, file=sys.stderr) # debugger
	conn = sqlite3.connect(cwd + "/" + sqlite_file)
	c = conn.cursor()
	exit_code = 0 # init exit_code var
	try:
		c.execute("""INSERT INTO url_data (unique_id, url, clicks) VALUES (?, ?, 0);""", [unique_id, url]) # inserts unique_id and url in db
		conn.commit() # commits the changes to the db
		exit_code = 1 # operation was successful
	except sqlite3.IntegrityError: # means that unique_id already exists because unique_id MUST be unique
		# add logging here
		print(e, file=sys.stderr) # debugger
		exit_code = 2 # operation was unsuccessful because of an IntegrityError
	except Exception as e: # unknown error
		# add loggin here
		print(e, file=sys.stderr) # debugger
		exit_code = 0 # operation was unsuccessful
	return exit_code # returns exit code for verification


""" Deletes a mapping in the database based on the unique id, removes all data and information """

def delete_url_mapping(unique_id):
	exit_code = 0 # init exit_code var
	conn = sqlite3.connect(cwd + "/" + sqlite_file)
	c = conn.cursor()
	try:
		c.execute("""DELETE FROM url_data WHERE unique_id = ?;""", [unique_id]) # removes all data from a given unique_id
		conn.commit() # commits changes to the database
		exit_code = 1 # operation was successful
	except Exception as e: # unknown error
		# add logging here
		print(e, file=sys.stderr) # debugger
		exit_code = 0 # operation was unsuccessful
	return exit_code # returns exit code for verification

""" Changes the url thats mapped to a specific unique_id, also clears all the clicks that the mapping held """

def alter_url_mapping(unique_id, new_url):
	conn = sqlite3.connect(cwd + "/" + sqlite_file)
	c = conn.cursor()
	exit_code = 0 # init exit_code var
	try:
		c.execute("""UPDATE url_data SET url = ? WHERE unique_id = ?;""", [new_url, unique_id]) # sets the new_url to existing url based on the unique_id given
		conn.commit() # commits the changes to the database 
		exit_code = 1 # operation was successful
	except Exception as e: # unknown error
		# add logging here
		print("Exception at alter_url_mapping => " + str(e), file=sys.stderr) # debugging for unsuccesfull operation
		exit_code = 0 # operation was unsuccessful
	return exit_code # returns the exit_code for further verification

""" Returns the click data based on a fiven unique_id """

def get_click_data(unique_id):
	conn = sqlite3.connect(cwd + "/" + sqlite_file)
	c = conn.cursor()
	try:
		c.execute("""SELECT clicks FROM url_data WHERE unique_id = ?""", [unique_id]) # selects the amount of clicks based on the given unique_id
		click_amount = c.fetchall()[0][0] # stores the clicks in variable: click_amount
		print("Click amount (from get_click_data): " + str(click_amount), file=sys.stderr) # debugger
		return click_amount
	except Exception as e:
		print("Exception at get_click_data: " + str(e), file=sys.stderr)
		return 0

""" Adds a new click to a url mapping """
""" Preconditon: unique_id must be valid """

def add_click(unique_id):
	conn = sqlite3.connect(cwd + "/" + sqlite_file)
	c = conn.cursor()
	exit_code = 0 # init exit_code var
	try:
		click_amount = get_click_data(unique_id) # runs get_click_data function to retrieve current number of clicks
		click_amount += 1 # increments the click_amount variable
		try:
			c.execute("""UPDATE url_data SET clicks = ? WHERE unique_id = ?;""", [click_amount, unique_id]) # updates the clicks in db with the new incremented click_amount
			conn.commit()
			exit_code = 1 # operation was unsuccessful
		except Exception as e: # unknown error
			exit_code = e # operation was unsuccessful
	except Exception as e: # unknown error
		exit_code = e # operation was successful
	return exit_code # returns back status of the operation/function for futher verification

""" Clears the click for a specific unique_id from the database """
""" Preconditon: unique_id must be valid """

def clear_click_data(unique_id):
	conn = sqlite3.connect(cwd + "/" + sqlite_file)
	c = conn.cursor()
	exit_code = 0 # init exit_code var
	try:
		c.execute("""UPDATE url_data SET clicks = ? WHERE unique_id = ?;""", [0, unique_id]) # update the click amount to 0 based on the given unique_id
		conn.commit()
		exit_code = 1 # operation was successful
	except Exception as e: # unknown error
		# add logging here
		print("Error from clear_click_data: " + str(e), file=sys.stderr)
		exit_code = 0 # operation was unsuccessful
	return exit_code # returns back satus of the operation/function for further verification

# --- ROUTES --- #

@app.route("/", methods=['GET'])
def index():
	# add logging here
	return render_template('index.html') # renders the index page for consumer / clients

@app.route("/a/<id>", methods=['GET']) # change to something shorter
def shortened_url_entry(id):
	id = str(id) # passes it as a string just in case
	add_click_ec = add_click(id) # adds click and returns the exit code
	print(add_click_ec, file=sys.stderr) # debugger
	# print("passed add click method", file=sys.stderr)
	if add_click_ec == 1: # adds a click and gets the exit code of the operation
		url = get_url(id) # gets the url that maps to the unique_id supplied
		print(url, file=sys.stderr)
		return redirect("http://" + url, code=303) # redirects the consumer to the real page 
	else: # adding a click didnt work
		# implement error handing for the server
		return "<center><h1>An Error Occured When Trying To Reach That URL</h1><p>- Apologies from Team Gup.py</p></center>" # explanation, method HAS to return somwthing or else an error will thrown

@app.route("/generateUrl", methods=['POST', 'GET'])
def generateUrl():
	if request.method == 'POST': # checks if a post request was made
		long_url = request.form['longUrl'] # retrieves the long_url from the request
		print(long_url, file=sys.stderr) # debugger
		unique_id = generate_unique_id() # generates a new unique_id
		print(unique_id, file=sys.stderr) # debugger
		short_url = "gup.py/a/" + unique_id # creates the short url based on the unique_id
		print(short_url, file=sys.stderr) # debugger
		create_url_mapping_ec = create_url_mapping(unique_id, long_url)
		if create_url_mapping_ec == 1: # creates the url mapping in DB and gets exit_code 
			return render_template("index.html", short_url=short_url, unique_id=unique_id) # renders the index page with new parameter
		else: # creating_the_url mapping didnt work
			# add error handling for this function , server side
			return render_template("changeUrl.html", error_response="An Error Occured, Sorry!") # re renders page with extra details
		
@app.route("/deleteUrl", methods=['POST', 'GET'])
def delete_url(): # deletes url
	if request.method == 'GET': # chekc sif the request being made is of a GET request
		return render_template("deleteUrl.html") # returns the 'homepage' of the Delete URL section
	elif request.method == 'POST': # checks if the request being made is of a POST request
		unique_id = request.form['uniqueID'] # gets the uniqueID thats held in the request'd form
		print("UniqueID found from deleteURL-POST method => " + str(unique_id), file=sys.stderr) # debugger to check the unique_id found
		delete_url_mapping_ec = delete_url_mapping(unique_id) # run the delete_url_mapping function and gets the exit code
		print("Delete_url_mapping_ec => " + str(delete_url_mapping_ec), file=sys.stderr) # debugger to cherck the exit_code given by the function
		if delete_url_mapping_ec == 1: # checks if the delete_url_mapping function was successfull
			return render_template("deleteUrl.html", delete_url_response="Deleted!") # re render the page with extra details
		else: # deleting the url mapping didnt work
			# add error handling here
			return render_template("changeUrl.html", change_url_response="An Error Occured, Sorry!") # re renders page with extra details

@app.route("/changeUrl", methods=['POST', 'GET'])
def change_url():
	if request.method == 'GET': # checks if the request is a GET request
		return render_template("changeUrl.html") # renders default changeUrl page
	elif request.method == 'POST': # chekcs if the request is a POST request
		unique_id = request.form['uniqueID'] # gets the uniqueID from request's from
		new_url = request.form['newUrl'] # gets the new url to map from the request's form
		clear_click_data_ec = clear_click_data(unique_id) # clears the click data linked to that unique ID
		if clear_click_data_ec == 1: # operation was successful
			alter_url_mapping_ec = alter_url_mapping(unique_id, new_url) # runs the alter_url_mapping function and gets exit_code
			if alter_url_mapping_ec == 1: # checks if there was a successful operation from the function
				return render_template("changeUrl.html", change_url_response="Successfully Changed, Link Now Goes To: " + str(new_url)) # re renders page with extra details
			else: # unsuccessful operation
				# add logging here
				print("change_url threw error in second else", file=sys.stderr)
				return render_template("changeUrl.html", change_url_response="An Error Occured, Sorry!") # re renders page with error response
		else: # clear_click_data was unsuccessful
			print("change_url threw error in first else", file=sys.stderr)
			return render_template("changeUrl.html", change_url_response="An Error Occured, Sorry!") # re renders page with extra details

@app.route("/checkStats", methods=['POST', 'GET'])
def check_stats():
	if request.method == 'GET':
		return render_template("checkStats.html")
	if request.method == 'POST':
		unique_id = request.form['uniqueID']
		get_click_data_ec = get_click_data(unique_id)
		if get_click_data_ec != 0: # operation was successful
			return render_template("checkStats.html", clicks=str(get_click_data_ec)) # re renders page with click data for users
		else: # operation unsuccessful
			# add logging here
			print("check_stats threw and error", file=sys.stderr) # debugger for errors
			return render_template("checkStats.html", error="An Error Occured, Sorry!") # re renders page with error response

if __name__ == '__main__':
	read_url_data() # reads the uel data before running application for debugging
	app.run(port=80,debug=True)
