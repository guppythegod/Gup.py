from flask import Flask, redirect, render
import sqlite3

""" url_Data
        | unique_id | url | clicks | 
"""
# --- SET UP --- #

app = Flask(__name__)
sqlite_file = "./url_db.sqlite"
table = "url_data"

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# --- MODULES --- #

""" Gets the url thats mapped to a a specific unique_id from the sqlite database """

def get_url(unique_id):
    c.execute("""SELECT url FROM url_data WHERE unique_id = s%""", (unique_id))
    return c.fetchall()
  
""" Generates a unique_id for a url, that is no present in the database """

def generate_unique_id():
    latest_id = int(json.load("metadata.json")["latest_id"])
    new_id += 1 if latest_id 

""" Creates a new mapping in the database with a unique_id and a url """

def create_url_mapping(unique_id, url):
    pass

""" Deletes a mapping in the database based on the unique id, removes all data and information """

def delete_url_mapping(uniue_id):
    pass

""" Changes the url thats mapped to a specific unique_id, also clears all the clicks that the mapping held """
def alter_url_mapping(unique_id, new_url):
    pass

""" Adds a new click to a url mapping """

def add_click(unique_id):
    pass
    
""" Clears the click for a specific unique_id from the database """

def clear_click_data(unique_id):
    pass

# --- ROUTES --- #

@app.route("/<str:id>")
def index(id):
    return_content = ""
    if id == "":
        # fix this, for some reason its not working 
        return_content = render("index.html")
    else:
        url = get_url(id)
        return_content = redirect(url, code=303)
    return return_content


if __name__ == '__main__':
    app.run()
