from sys import exit

people = {
    "EMMA" : "617-555-0100",
    "RODRIGO" : "617-55-0102",
    "BRIAN" : "617-55-0102",
    "DAVID" : "617-555-0103"
}

if "EMMA" in people:
    print(f"Found {people['EMMA']}")
    exit(0)
print("Not found")
exit(1)