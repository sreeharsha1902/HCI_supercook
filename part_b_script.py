a = input('give the location of the file')
file = open(a, "r")

data = file.read()

occurrences = data.count("click")
print('number of clicks :', occurrences)
