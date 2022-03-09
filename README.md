# cs5293sp22-project0

### Author: Sarah Brown

# Directions to Install and Use Package
To download and use package, follow the steps below:

1. git clone https://github.com/SarahBrown/cs5293sp22-project0.git
2. cd cs5293sp22-project0/
3. pipenv install

4. Step 4 can be run in either of the below ways depending on whether a local file is being used for testing or if an url is being input instead.
* pipenv run python project0/main.py --incidents resources/2022-02-01_daily_incident_summary.pdf 
* pipenv run python project0/main.py --incidents <url>

# Web or External Libraries
For this project I used several packages from the standard library and some external libraries. These included argparse, os, re, sqlite3, and urllib. In addition, PyPDF2 was an external library that was imported.

# Functions and Approach to Development
This project uses various functions to extract information from a pdf and store the information. 

## Download Data
The download function takes an url and downloads a PDF from the Norman police department's website. First, the function checks to see if the url contains "http." If it does contain it, the function downloads the PDF, saves it, and returns the file location in the resources folder. If it does not contain http, the function simply returns the passed url as a file location as it is a local file for testing purposes. 

The downloaded data file are stored in the project file system in a resources folder. Test files used for pytests are also stored here. Although originally I stored the files in the /tmp directory, I switched to a resources folder in the project files to allow for using Github Actions with PyTest.

## Extract Data
The extract incidents function imports the PDF file with a pdfReader object and processes all of its pages. It loops through the pages with different cases for the first page and the last page. The first page and the last page have title information, column information, and footer information that needs to be removed. This is done by using a regular expression and splitting the string from the PDF page based on the date.  The first page and the last page have parts of this ignored due to the extra content. 

Splitting based on date then gives a list that has a date and an additional string per incident. The number of incidents per page can be found by dividing by 2. These strings can then be looped over to further split based on "/n" newline characters. There are then three cases taken into account, the standard case, the double lined location case, and the case where the location and nature of incident are blank. These can be identifed by the number of newline characters left in the string after splitting based on date. If the location and the nature of the incident are blank, these are filled in with "Unknown" to ensure proper database creation in addition to acknowledging that the data is missing. 

The filtered information is then stored in a list and added to a larger incidents list which is returned at the end of the function. This function also takes in a testing boolean. Testing is set to true in the Pytest to check the status function. This forces the page length to be extracted to be 2 pages, a number of pages where the incidents can easily be confirmed by hand.

## Create Database
The create database function creates an SQLite database file named normanpd.db in the resources folder. Before creating this database file, the function checks to see if the datapath already exists. If the datapath does already exists, it is removed before a new version is created. The database then inserts a table with a given schema for the incident details.

## Populate Database
The populate database function takes the extracted incidents and adds them to the created table. This is done using the insertmany command to avoid loops.

## Database Status
The database status function connects to the created database and selects the nature of the incidents and counts the number of times they have occurred. The list is sorted by the total number first and alphabetically by the nature second. When the print status is requested, i.e. when testing is not occuring, the results are then formatted and printed. When tests are done, the print statements are repressed to avoid potential issues with the Github Actions interface.

# Assumptions Made and Known Bugs
There were several assumptions made while extracting data from the PDFs. The first of which was that only the location or the nature could be blank. This assumption was made based on observations of various report examples. In addition, I assumed that if one of the two were blank, then both of them were blank. This was to combat the possibility of a double lined address combined with a blank incident nature. This case would be indistinguishable from the standard case. Finally, I also assumed that the location was the only type that could result in a double lined entry.

There are no known bugs.

# Tests
Tests are performed with PyTest and local data. Tests are also set up with Github Actions and PyTest to run automatically when code is pushed to the repository. 

## Test Download
Downloading via url was tested by hand as files are removed from the website. Loading a local file was tested by confirming that the filename returned by the download function was the same as the one that was passed into the function.

## Test Extract Incidents
The extract incidents file was testing by passing in a locally stored PDF file and comparing the results. First, the number of extracted events was compared against the known number of extracted events for a specific PDF file. Second, the various cases were tested to make sure that they were handled properly. Four incidents were selected, the first entry, the last entry, an entry with blank location and nature of incident, and an entry with a location spanning two lines. Each of these incidents were compared to their expected results.

## Test Create Database
To test the creation of the database, first the create database function was tested. Following that, it was confirmed that the filepath existed. After the table was confirmed to exist, the table name and the table column names were confirmed to have been labeled correctly.

## Test Populate Data
To test that the data was populated correctly, the incidents were extracted and inserted into a database. It was then asserted that the number of entries in the table and the number of incidents matched.

## Test Status
The status function was tested by passing in a two page PDF and creating an incidents database for it. Since this PDF was shorter than the usual ones, it was easy to count the number of incidents by hand to create test data to confirm against. This two page PDF was created via a boolean flag passed into the extract incidents function.