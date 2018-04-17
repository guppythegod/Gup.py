"""
ONLY RUN THIS FILE WHEN YOU HAVE TO START THE DATABASE OVER FROM SCRATCH, RUNNING THIS FILE WHEN THERE ALREADY IS A url_db.sqlite FILE IN THE DIRECTORY
WILL RESULT IN AN ERROR AS THE TABLE ALREADY EXISTS, USE COMMON SENSE.
"""

import sqlite3
import os

sqlite_file = "url_db.sqlite"
cwd = os.path.dirname(os.path.realpath(__file__))
print(cwd)
conn = sqlite3.connect(cwd + "/" + sqlite_file)
c = conn.cursor()

# Creates table, 'url_data' with neccessary columns and keys
c.execute("""CREATE TABLE url_data(unique_id TEXT NOT NULL, url TEXT NOT NULL, clicks INT NOT NULL, PRIMARY KEY (unique_id));""")

conn.commit() # commit the changes to the db
conn.close() # close the database