from flask import Flask, redirect, render_template, request, json
import sqlite3
import os

""" 

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
	try:
		c.execute("""SELECT url FROM url_data WHERE unique_id = %s;""", [unique_id]) # gets the url from the unique_id
		return str(c.fetchall()) # returns back that the query retrieved from the db as a str (just incase)
	except Exception as e: # Unknown error
		return 0 # operation was unsuccessful so send back exit_code=0
  
""" Generates a unique_id for a url, that is no present in the database 

def generate_unique_id():
	latest_id = int(json.load("metadata.json")["latest_id"])
	new_id += 1 if latest_id 
"""
""" Creates a new mapping in the database with a unique_id and a url """

def create_url_mapping(unique_id, url):
	exit_code = 0 # init exit_code var
	try:
		c.execute("""INSERT INTO url_data (unique_id, url, clicks) VALUES (?, ?, 0);""", [unique_id, url]) # inserts unique_id and url in db
		conn.commit() # commits the changes to the db
		exit_code = 1 # operation was successful
	except sqlite3.IntegrityError: # means that unique_id already exists because unique_id MUST be unique
		# add logging here
		print(e)
		exit_code = 0 # operation was unsuccessful
	except Exception as e: # unknown error
		# add loggin here
		print(e)
		exit_code = 0 # operation was unsuccessful
	return exit_code # returns exit code for verification


""" Deletes a mapping in the database based on the unique id, removes all data and information """

def delete_url_mapping(unique_id):
	exit_code = 0 # init exit_code var
	try:
		c.execute("""DELETE FROM url_data WHERE unique_id = ?;""", [unique_id]) # removes all data from a given unique_id
		conn.commit() # commits changes to the database
		exit_code = 1 # operation was successful
	except Exception as e: # unknown error
		# add logging here
		print(e)
		exit_code = 0 # operation was unsuccessful
	return exit_code # returns exit code for verification

""" Changes the url thats mapped to a specific unique_id, also clears all the clicks that the mapping held """

def alter_url_mapping(unique_id, new_url):
	exit_code = 0 # init exit_code var
	try:
		c.execute("""UPDATE url_data SET url = (%s) WHERE unique_id = (%s);""", [new_url, unique_id]) # sets the new_url to existing url based on the unique_id given
		conn.commit() # commits the changes to the database 
		exit_code = 1 # operation was successful
	except Exception as e: # unknown error
		# add logging here
		exit_code = 0 # operation was unsuccessful
	return exit_code # returns the exit_code for further verification

""" Adds a new click to a url mapping """
""" Preconditon: unique_id must be valid """

def add_click(unique_id):
	exit_code = 0 # init exit_code var
	try:
		c.execute("""SELECT clicks FROM url_data WHERE unique_id = %s;""", [unique_id]) # selects the amount of clicks based on the given unique_id
		click_amount = c.fetchall() # store the clicks in variable: click_amount
		click_amount += 1 # increments the click_amount variable
		try:
			c.execute("""UPDATE url_data SET clicks = (%s) WHERE unique_id = (%s);""", [click_amount, unique_id]) # updates the clicks in db with the new incremented click_amount
			conn.commit()
			exit_code = 1 # operation was unsuccessful
		except Exception as e: # unknown error
			exit_code = 0 # operation was unsuccessful
	except Exception as e: # unknown error
		exit_code = 0 # operation was successful
	return exit_code # returns back status of the operation/function for futher verification
	

""" Clears the click for a specific unique_id from the database """
""" Preconditon: unique_id must be valid """

def clear_click_data(unique_id):
	exit_code = 0 # init exit_code var
	try:
		c.execute("""UPDATE url_data SET clicks = (%s) WERE unique_id = (%s);""", [0, unique_id]) # update the click amount to 0 based on the given unique_id
		conn.commit()
		exit_code = 1 # operation was successful
	except Exception as e: # unknown error
		# add logging here
		exit_code = 0 # operation was unsuccessful
	return exit_code # returns back satus of the operation/function for further verification

# --- ROUTES --- #

@app.route("/")
def index():
	# add logging here
	return render_template('index.html') # renders the index page for consumer / clients

@app.route("/a/<id>") # change to something shorter
def shortened_url_entry(id):
	id = str(id) # passes it as a string just in case
	if add_click(id) == 1: # adds a click and gets the exit code of the operation
		url = get_url(id) # gets the url that maps to the unique_id supplied
		return redirect(url, code=303) # redirects the consumer to the real page 
	else: # adding a click didnt work
		# implement error handing for the server
		pass

@app.route("/generateUrl", methods=['POST', 'GET'])
def generateUrl():
	if request.method == 'POST': # checks if a post request was made
		long_url = request.form # retrieves the long_url from the request
		unique_id = generate_unique_id() # generates a new unique_id
		short_url = "gup.py/a/" + unique_id # creates the short url based on the unique_id
		if create_url_mapping(unique_id, long_url) == 1: # creates the url mapping in DB and gets exit_code 
			return render_template("index.html", short_url=short_url, unique_id=unique_id) # renders the index page with new parameter
		else: # creating_the_url mapping didnt work
			# add error handling for this function , server side
			pass
		
if __name__ == '__main__':
	app.run(port=80,debug=True)

	
