filename = input("filename: ") + ".txt"
if filename == "r.txt":
    filename = "results.txt"
file = open(filename, "r")
dict = {}

for line in file.readlines():
    if not "[" in line:
        if not line in dict:
            dict[line] = 1
        else:
            dict[line] += 1

for num in dict:
    print(str(num) + ": " + str(dict[num]))
file.close()