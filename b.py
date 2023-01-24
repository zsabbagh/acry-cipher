f = open('letter.data', 'r').read().rstrip().split('\n')

l = []

for i in range(0, len(f)):
    pass

l = sorted(l, key=lambda x : x[1], reverse=True)

for x in l:
    print(x[0])

