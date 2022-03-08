import argparse

import project0

def main(url):
    # Download data or load local file
    filename = project0.download(url)

    # Extract data
    testing = False # if testing status, only reads in first 2 pages
    incidents = project0.extractincidents(filename, testing)
	
    # Create new database
    db = project0.createdb()
	
    # Insert data
    project0.populatedb(db, incidents)
	
    # Print incident counts and stores results in variable for testing
    print_status = True
    results = project0.status(db, print_status)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)