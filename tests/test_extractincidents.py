from project0 import project0

def test_extractincidents():
    incidents = project0.extractincidents("resources/2022-02-01_daily_incident_summary.pdf")

    num_incidents = 392
    incident0 = ["2/1/2022 0:04","2022-00001588","15300 E LINDSEY ST","MVA With Injuries","14005"] # first entry
    incident16 = ["2/1/2022 1:18","2022-00001591","1712 VIRGINIA ST","Diabetic Problems","14005"] # first entry, second page
    incident154 = ["2/1/2022 11:48","2022-00005722","W LINDSEY ST / I35 NB OFF RAMP 108B EAST SPUR RAMP RAMP","COP Relationships","OK0140200"] # double lined address
    incident205 = ["2/1/2022 13:30","2022-00002100","Unknown","Unknown","EMSSTAT"] # blank address and nature
    incident391 = ["2/1/2022 23:56","2022-00005883","4409 132ND AVE SE","Supplement Report","OK0140200"] # last entry

    # check length of incidents
    assert len(incidents) == num_incidents

    # check different incidents to make sure created properly
    assert incidents[0] == incident0
    assert incidents[16] == incident16
    assert incidents[154] == incident154
    assert incidents[205] == incident205
    assert incidents[391] == incident391

