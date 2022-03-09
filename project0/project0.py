import os
import PyPDF2
import re
import sqlite3
import urllib.request


def download(url):
    """
    Download function to prepare pdf for processing.
    Checks to see if file is local or if it needs to be downloaded.
    
    Parameters
    ----------
    url : str
        The url to download or location of local file.

    Returns
    -------
    filename
        Location of file in resources folder.
    """
    # headers for request so not to spam website
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"

    # check to see if http is included in the url
    # if http is included, need to download pdf
    if "http" in url[0:4]:
        data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()
        filename = "resources/" + url.split("/")[-1]

        # open a file with filename and write binary content. will overwrite any previous content.
        f = open(filename, "wb") 
        f.write(data)
        f.close()
    else:
        filename = url

    return filename

def extractincidents(filename, testing):
    """
    Function to remove separate incidents from pdf.
    
    Parameters
    ----------
    filename : str
        Location of file in resources folder.
    
    testing: boolean
        Boolean flag to determine page count used. 
        Two pages used during testing as that could be hand counted.

    Returns
    -------
    incidents
        List of incidents extracted from the pdf.
    """
    incidents = list() # creates empty list to store incidents from pdf file

    # opens pdf file, creates a pdfReader, and stores page count
    pdf_file = open(filename, "rb")
    pdfReader = PyPDF2.pdf.PdfFileReader(pdf_file)
    page_count = pdfReader.getNumPages()

    # only reads in first two pages if testing status
    if testing:
        page_count = 2

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
    """
    Function to create sqlite database based.

    Returns
    -------
    db_filename
        Location of database in resources folder.
    """
    db_filename = "resources/normanpd.db"

    # removes old database created under same name if it exists
    if os.path.exists(db_filename):
        os.remove(db_filename)

    # connect to database and creates it (since deleted if it did exist)
    connection = sqlite3.connect(db_filename)
    connection.execute("CREATE TABLE incidents (incident_time TEXT,incident_number TEXT,incident_location TEXT,nature TEXT,incident_ori TEXT);")

    # commit the changes to db and close the connection
    connection.commit()
    connection.close()

    return db_filename


def populatedb(db, incidents):
    """
    Function to populate database.
    
    Parameters
    ----------
    db: str
        Location of database in resources folder.
    
    incidents: list
        Extracted incidents to insert into database.
    """
    # opens connection and gets cursor
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    # insert the list of incidents into db
    cursor.executemany("INSERT INTO incidents VALUES(?,?,?,?,?);", incidents)
    #print('We have inserted', cursor.rowcount, 'records to the table.')

    # commit the changes to db and close the connection
    connection.commit()
    connection.close()


def status(db, print_status):
    """
    Function to report database status.
    
    Parameters
    ----------
    db : str
        Location of file in resources folder.
    
    print_status: boolean
        Boolean flag to determine if status should be printed. 
        Printing is disabled during testing to avoid any potential errors.

    Returns
    -------
    results
        Status report in list form.
    """
    # opens connection and gets cursor
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    # selects from nature and groups based on count of nature and sorts
    cursor.execute("SELECT nature, count(nature) FROM incidents GROUP BY nature ORDER BY count(nature) DESC, nature") 
    results = cursor.fetchall()

    connection.close()

    # if requested, print status. flag added to avoid printing during testing
    if (print_status):
        for result in results:
            print(result[0]+"|"+str(result[1]))

    return results