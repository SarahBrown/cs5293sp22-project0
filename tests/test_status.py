from project0 import project0

def test_status():
    # loads a shorter 3 page pdf to test against into a db
    incidents = project0.extractincidents("resources/2022-02-01_daily_incident_summary.pdf", True)
    db = project0.createdb()
    project0.populatedb(db, incidents)

    # stores results to check against
    print_status = False
    results = project0.status(db, False)

    known_results = [('Traffic Stop', 8),('Contact a Subject', 4),('MVA With Injuries', 3),('Breathing Problems', 2),('Chest Pain', 2),('Diabetic Problems', 2),('Fire Alarm', 2), 
        ('Disturbance/Domestic', 1),('Extra Patrol', 1),('Fraud', 1),('Larceny', 1),('Pick Up Items', 1),('Suspicious', 1),('Transfer/Interfacility', 1),('Trespassing', 1),('Welfare Check', 1)]

    # checks that number of incidents from input equals number of rows added to table
    assert results == known_results

