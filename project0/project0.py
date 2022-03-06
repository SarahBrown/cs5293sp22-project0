import urllib.request
import PyPDF2
import tempfile
import re
import sqlite3
import os

def download(url):
    # headers for request so not to spam website
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"

    # check to see if http is included in the url
    # if http is included, need to download pdf
    if "http" in url[0:4]:
        data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()
        filename = "/tmp/" + url.split("/")[-1]

        # open a file with filename and write binary content. will overwrite any previous content.
        f = open(filename, "wb") 
        f.write(data)
        f.close()
    # if http is not included, load local file
    else:
        filename =  "/tmp/" + url

    return filename

def extractincidents(filename):
    incidents = list() # creates empty list to store incidents from pdf file

    # opens pdf file, creates a pdfReader, and stores page count
    pdf_file = open(filename, "rb")
    pdfReader = PyPDF2.pdf.PdfFileReader(pdf_file)
    page_count = pdfReader.getNumPages()

    for pagenum in range(page_count):
        page = pdfReader.getPage(pagenum).extractText()
        page = re.split(r"([0-9]*/[0-9]*/[0-9]* [0-9]*:*[0-9]*:*[0-9]*)", page)

        # removes misc info from first page if current page is first page
        if pagenum == 0:
            page = page[1:] # removes column headers for first page
            page[-1] = page[-1].replace("NORMAN POLICE DEPARTMENT\nDaily Incident Summary (Public)\n", "") # removes title header

        # removes footer info from last page
        if pagenum == page_count-1:
            page = page[0:-1]
        page = list(filter(None, page)) # removes any empty entries, happens on pages after first page where column headers would be
        num_incidents_page = int(len(page)/2) # counts number of incidents on page
        
        # loops through each incident to add information to incidents list
        for incid in range(num_incidents_page):
            incid_details = list()
            incid_details.append(page[incid*2])
            non_date_details = page[incid*2+1]
            non_date_details = list(filter(None, non_date_details.split("\n")))
            entries = len(non_date_details)
            incid_details.append(non_date_details[0])
            non_date_details.pop(0)

            # if the only entries were date, incident #, and incident ori
            if len(non_date_details) == 1:
                # fills in unknown for location and nature
                incid_details.append("Unknown") 
                incid_details.append("Unknown")
                incid_details.append(non_date_details[-1])

            # double lined location
            elif len(non_date_details) == 4:
                incid_details.append(non_date_details[0]+non_date_details[1])
                incid_details.append(non_date_details[2])
                incid_details.append(non_date_details[3])

            # standard case
            else:
                incid_details.append(non_date_details[0])
                incid_details.append(non_date_details[1])
                incid_details.append(non_date_details[2])

            incidents.append(incid_details)
    return(incidents)

def createdb():
    db_filename = "/tmp/normanpd.db"

    # removes old database created under same name if it exists
    if os.path.exists(db_filename):
        os.remove(db_filename)

    # connect to database and creates it (since deleted if it did exist)
    connection = sqlite3.connect(db_filename)
    connection.execute(''' CREATE TABLE incidents (
        incident_time TEXT,
        incident_number TEXT,
        incident_location TEXT,
        nature TEXT,
        incident_ori TEXT);''')

    # commit the changes to db and close the connection
    connection.commit()
    connection.close()

    return db_filename


def populatedb(db, incidents):
    # opens connection and gets cursor
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    # insert the list of incidents into db
    cursor.executemany('INSERT INTO incidents VALUES(?,?,?,?,?);', incidents); #need semicolon??????
    #print('We have inserted', cursor.rowcount, 'records to the table.')

    # commit the changes to db and close the connection
    connection.commit()
    connection.close()


def status(db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute('SELECT nature, count(nature) FROM incidents GROUP BY nature ORDER BY count(nature) DESC, nature') 
    results = cursor.fetchall()

    for result in results:
        print(result[0]+"|"+str(result[1]))
