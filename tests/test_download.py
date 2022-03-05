from project0 import project0

def test_download():
    download_url = "https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-25_daily_incident_summary.pdf"
    saved_file = "2022-02-01_daily_incident_summary.pdf"

    filename_download = project0.download(download_url)
    filename_saved = project0.download(saved_file)

    assert filename_download == "/tmp/2022-02-25_daily_incident_summary.pdf"
    assert filename_saved == "/tmp/2022-02-01_daily_incident_summary.pdf"