import random,math
from statistics import mean
typelist=["Student","Housewife","Blue_collar"]
#"AFF","White_collar","Inoccupation","Self_employment"

def human_generate(N,gausmean,type,seed):
    hlist=[]    
    random.seed(seed) 
    standard=int(gausmean*N)
    for _ in range(N):#랜덤리스트 생성
        val = random.gauss(gausmean,1)
        if val <= 0.5:
            val = 1
        hlist.append(round(val))

    if sum(hlist)>standard:
        val=sum(hlist)-standard
        for i in range(val):
            dec_mean(hlist,i)
    else:
        val=standard-sum(hlist)
        for i in range(val):
            inc_mean(hlist,i)

    with open("population/nof_fam{0}_{2}{1}.txt".format(N,seed,type), 'w') as f:
        family=0
        buildingcount=0
        fam_per_building=b_percent(random.random())
        id=0
        for item in hlist:
            family+=1
            for __ in range(item):
                if __==item-1:
                    id+=1
                    f.write("%s(%d)\n"% (type,id))
                else:
                    id+=1
                    f.write("%s(%d)," % (type,id))
            buildingcount+=1
            if buildingcount >fam_per_building:
                buildingcount=0
                fam_per_building=b_percent(random.random())
                f.write("\n")
    
            

def b_percent(percentage):
    if percentage <= 0.815269: #아파트
        return random.gauss(87.56421032,1)
    elif percentage <=0.947178: #원룸
        return random.gauss(4.229920039,1)
    elif percentage <=0.984548: #단독주택
        return random.gauss(1.556705162,1)      
    elif percentage <=0.992881: #빌라
        return random.gauss(11.14336891,1)      
    elif percentage <=0.999113: #원룸 (작은빌라)
        return random.gauss(3.623493646,1)      

    elif percentage <=0.999856:#다중주택
        return random.gauss(2.483808026,1)      
    else:  #공관
        return random.gauss(3.826589521,1)      

    
def dec_mean(list,index):
    if list[index]<2:
        dec_mean(list,index+1)
    else:
        list[index]-=1

def inc_mean(list,index):
    if list[index]>5:
        dec_mean(list,index+1)
    else:
        list[index]+=1

#testcode
"""
for type in typelist:
    for i in range(1):
        human_generate(3725,2.6848,type,i)
        print("%d works left",31-i)
"""
for type in typelist:
    for i in range(1,31):
        human_generate(3725,2.6848,type,i)
        print("%d works left",31-i)

for type in typelist:
    for i in range(1,31):
        human_generate(3725,2.6848,type,i)
        print("%d works left",31-i)
"""
[AFF,Student,Housewife,Blue_collar,White_collar,Inoccupation,Self_employment]
if sum(hlist)>standard:
        val=sum(hlist)-standard
        for i in range(val):
            dec_mean(hlist,i)
    else:
        val=standard-sum(hlist)
        for i in range(val):
            inc_mean(hlist,i)
    print(len(hlist))

"""