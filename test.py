import re
list = re.findall('\d+', "Must be delivered with 15, 19")
for i in range(0, len(list)):
    list[i] = int(list[i])
print(list)