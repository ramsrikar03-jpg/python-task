def read_file():
    f = open("log.txt", "r")
    for line in f:
        yield line.strip()
count = {}
for line in read_file():
    if "ERROR" in line: 
        if line in count:
            count[line] += 1
        else:
            count[line] = 1
for key in count:
    print(key, ":", count[key])