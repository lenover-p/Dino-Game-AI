list = []
for i in range(2):
    list.append([3])

list[0] = [0]
list[1] = [1]
print(list[1][0])