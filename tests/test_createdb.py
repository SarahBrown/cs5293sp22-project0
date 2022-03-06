from project0 import project0
import os

def test_createdb():
    db = project0.createdb()

    # checks to see if db file was created
    assert os.path.exists("/tmp/normanpd.db")

    # checks to see if returned file name is correct
    assert db == "/tmp/normanpd.db"