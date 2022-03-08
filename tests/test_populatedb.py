from project0 import project0

import sqlite3

def test_populatedb():
    # gets incidents, creates db, and populates db
    incidents = project0.extractincidents("resources/2022-02-01_daily_incident_summary.pdf", False)
    db = project0.createdb()
    project0.populatedb(db, incidents)

    # checks that number of incidents from input equals number of rows added to table
    connection = sqlite3.connect("resources/normanpd.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM incidents") # fetches all rows
    results = cursor.fetchall()
    connection.close()

    assert len(results) == len(incidents) # compares lengths