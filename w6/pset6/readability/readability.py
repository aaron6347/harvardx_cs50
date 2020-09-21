st = input("Text: ")
l = w = s = 0
for each in st:
    if each.isalpha():
        l += 1
    elif each in [" "]:
        w += 1
    elif each in [".", "!", "?"]:
        s += 1
# last word in text not using space but fullstop
w += 1
# index
i = round(0.0588 * (l/w)*100 - 0.296 * (s/w)*100 - 15.8)
if i < 1:
    print("Before Grade 1")
elif i >= 16:
    print("Grade 16+")
else:
    print("Grade", i)