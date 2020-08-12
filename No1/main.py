from functools import reduce

def name_sum(name):
    return reduce(lambda prev, cur: prev + ord(cur) - 64, name, 0)

# read list names from file
with open('names.txt', 'r') as f:
    names = f.read().replace('"', '').split(',')

sort_names = sorted(names)

# calc 4 res
res = 0
for i, name in enumerate(sort_names):
    res += name_sum(name) * (i + 1)

print(res)