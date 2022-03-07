from project0 import project0

def test_download():
    download_url = "https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-25_daily_incident_summary.pdf"
    
    filename_download = project0.download(download_url)

    assert filename_download == "resources/2022-02-25_daily_incident_summary.pdf"
