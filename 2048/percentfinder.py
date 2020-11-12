file = open("results.txt", "r")

dict = {}

for line in file:
    if not line in dict:
        dict[line] = 1
    else:
        dict[line] += 1

total = 0
goodtotal = 0
for num in dict:
    print(str(num) + ": " + str(dict[num]))
    total += dict[num]
    if int(num) >= 2048:
        goodtotal += int(dict[num])

print("Good percentage: " + str(goodtotal / total))

file.close()
