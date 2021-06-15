n = int(input())

x = 0
while x < n:
    msg = input()
    # Can we use split here?
    print(msg)
    x = x + 1

goto = input()
# We only need to look at the third word in this, every time!
print(goto)
print(goto.split())
print(goto.split()[2])
