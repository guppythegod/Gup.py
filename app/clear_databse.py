"""
ONLY RUN THIS FILE WHEN YOU HAVE TO REMOVE ANY EXISTING url_data TABLES IN DB
"""

import sqlite3
import os

sqlite_file = "url_db.sqlite"
cwd = os.path.dirname(os.path.realpath(__file__))
print(cwd)
conn = sqlite3.connect(cwd + "/" + sqlite_file)
c = conn.cursor()
c.execute("""DROP TABLE url_data""")
conn.commit() # commit the changes to the db
conn.close() # close the database
