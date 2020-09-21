invalid = True
while(invalid):
    number = input("Number: ")
    # if there is any none numeric in input
    for ind, x in enumerate(number):
        if not x.isnumeric():
            invalid = True
            break
        elif ind == len(number)-1:
            invalid = False

output = ''
# get header
header = int(number[:2])
# check type
if (header == 34 or header == 37) and len(number) == 15:
    output = "AMEX"
elif (header >= 51 and header <= 55 and len(number) == 16):
    output = "MASTERCARD"
elif (header//10 == 4 and (len(number) == 13 or len(number) == 16)):
    output = "VISA"
else:
    print("INVALID")
    exit()
# check luhn algo
sum1 = sum2 = 0
for ind, val in enumerate(reversed(number)):
    if ind % 2 != 1:
        sum2 += int(val)
    else:
        temp = int(val)*2
        if temp > 9:
            sum1 += 1
        sum1 += (temp % 10)
if (sum1 + sum2) % 10 == 0:
    print(output)