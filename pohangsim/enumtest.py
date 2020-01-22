blist=[]
hlist=[]
fam=[]
file = open('population/nof_fam3725_Blue_collar1.txt','r')
lines = file.readlines()
file.close()
for i in range(len(lines)):  
    line = lines[i].split('\n')[0]
    if not line == "":
        elements = (line.split(','))
        for j in elements:
            fam.append(eval(j))
            hlist.append(fam)
            fam=[]
        if i == len(lines)-1:
            blist.append(hlist)
            hlist = []
    else:
        blist.append(hlist)
        hlist = []
[e for e in enumerate([0.1 for building in blist])]