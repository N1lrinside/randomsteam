import re
m=input()
h=re.search(r'/id/', m)
print(h.span()[1])