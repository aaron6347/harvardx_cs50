from sys import argv, exit
import csv
# validate argument
if len(argv) != 3:
    print("Usage: python dna.py data.csv sequences.txt")
    exit(1)
else:
    # open and read csv
    try:
        with open(argv[1], 'r') as file:
            reader = csv.DictReader(file)
            header = reader.fieldnames
            data = [row for row in reader]
    # if file doesnt exist
    except FileNotFoundError as e:
        print("{} is not found.".format(argv[1]))
        exit(1)

    # open and read txt
    try:
        with open(argv[2], 'r') as file2:
            seq = file2.readline()
    # if file doesnt exist
    except FileNotFoundError as e:
        print("{} is not found.".format(argv[2]))
        exit(1)

    # store sequence result
    ar = []
    # repeatedly finding each str in the sequence
    for strs in header[1:]:
        maxx = num = i = 0
        while (i < len(seq)):
            pattern = seq[i:len(strs)+i]
            # if the current number is better than previous highest count than save this newest count
            if num > maxx:
                maxx = num
            # if the str is found, skip the current position by using length of str
            if pattern == strs:
                num += 1
                i += len(strs)
            # if str is not found or consecutive pattern drops, make number to 0 and increment position by 1
            else:
                num = 0
                i += 1
        # save result
        ar.append(str(maxx))

    # iterate each data
    for row in data:
        # iterate each str
        for ind, fieldname in enumerate(header[1:]):
            # if the result and data isnt the same, skip the its other str
            if row[fieldname] != ar[ind]:
                break
            # if the result and data is the same and this is the last data to be checked, this is the owner of the dna sequence
            elif row[fieldname] == ar[ind] and ind == len(header[1:])-1:
                print(row[header[0]])
                exit(0)
    # if there is no data with such str result
    print("No match")
    exit(0)