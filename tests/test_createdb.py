from project0 import project0

import os
import sqlite3

def test_createdb():
    db = project0.createdb()

    # checks to see if db file was created
    assert os.path.exists("resources/normanpd.db")

    # checks to see if returned file name is correct
    assert db == "resources/normanpd.db"

    # check to see if table was created correctly
    connection = sqlite3.connect("resources/normanpd.db") 
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master") # gets table name
    name_result = cursor.fetchall()
    name_result = (name_result[0])[0]
    assert name_result == "incidents" # checks that table was named correctly

    # check columns
    row = cursor.execute("PRAGMA table_info('incidents')").fetchall() # gets table infos
    columns = []
    for r in row:
        columns.append(r[1]) # puts column names in list
        
    assert columns == ["incident_time", "incident_number", "incident_location", "nature", "incident_ori"]

    connection.close()