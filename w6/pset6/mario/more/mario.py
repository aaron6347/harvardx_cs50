while(True):
    height = input('Height: ')
    if not height.isnumeric():
        continue
    height = int(height)
    if height >= 1 and height <= 8:
        break
place = 1
for row in range(height):
    output = ''
    for pos in range(height):
        if height - pos <= place:
            output += '#'
        else:
            output += ' '
    output += '  '
    for pos in range(place):
        output += "#"
    print(output)
    place += 1