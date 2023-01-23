f = open('bigram', 'r').read().rstrip().replace('%','').replace('\n', ' ').split(' ')

l = []

for i in range(1, len(f)):
    if f[i-1] != '' and f[i] != '':
        try:
            l.append([f[i-1], float(f[i])])
        except:
            l.append([f[i], float(f[i-1])])

l = sorted(l, key=lambda x : x[1], reverse=True)

for x in l:
    print(x[0])

