from project0 import project0

def test_download():
    saved_url = "resources/2022-02-01_daily_incident_summary.pdf"
    filename_saved = project0.download("2022-02-01_daily_incident_summary.pdf")

    assert filename_saved == saved_url