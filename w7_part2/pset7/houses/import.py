# TODO
import csv
from sys import argv, exit
import cs50

# open students.db
db = cs50.SQL("sqlite:///students.db")

# validate argument
if len(argv) != 2:
    print("Usage: python import.py data.csv")
    exit(1)
else:
    # if data file exist
    try:
        with open(argv[1]) as file:
            reader = csv.DictReader(file)
            ar = []
            for row in reader:
                og_name = row['name']
                # split name into first, middle, last
                ar = og_name.split(' ')
                first = ar[0]
                middle = None
                last = ar[len(ar)-1]
                house = row['house']
                birth = row['birth']
                # if the ar has 3 element means there is middle name
                if len(ar) == 3:
                    middle = ar[1]
                # insert data into db
                db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)",
                           first, middle, last, house, birth)
    # if data file doesnt exist
    except FileNotFoundError as e:
        print("{} file doesn't exist".format(argv[1]))
        exit(1)
