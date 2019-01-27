from sys import argv

with open(argv[1]) as f:
    content = [l.strip() for l in f]
    content.sort()

for c in content:
    print(c)