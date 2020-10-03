# TODO
import csv
from sys import argv, exit
import cs50

# open students.db
db = cs50.SQL("sqlite:///students.db")

# validate argument
if len(argv) != 2:
    print("Usage: python roster.py 'House'")
    exit(1)
else:
    # get all houses exist in db
    db_houses = db.execute("SELECT DISTINCT(house) FROM students")
    ar_houses = [each['house'] for each in db_houses]
    # if find roster before import data or database has no data
    if len(ar_houses) == 0:
        print("No data is detected, please import data into database first")
        exit(1)
    # if wrong input house
    elif argv[1] not in ar_houses:
        print("{} House doesn't exist in database".format(argv[1]))
        exit(1)
    # if house does exist in database
    else:
        # get all data of the specific house
        all_data = db.execute("SELECT * FROM students WHERE house = \"{}\" ORDER BY last ASC, first ASC".format(argv[1]))
        # print output
        for each in all_data:
            if each['middle'] != None:
                print("{} {} {}, born {}".format(each['first'], each['middle'], each['last'], each['birth']))
            else:
                print("{} {}, born {}".format(each['first'], each['last'], each['birth']))
