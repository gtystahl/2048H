file = open("100results.txt")

dict = {}

for line in file:
    if not line in dict:
        dict[line] = 1
    else:
        dict[line] += 1

for num in dict:
    print(str(num) + ": " + str(dict[num]))
