import random,math
from statistics import mean
typelist=["Student","Housewife","Blue_collar"]
#"AFF","White_collar","Inoccupation","Self_employment"

#학생이 20%인 리스트를 만들어서 하나씩 pop 한다

def population_ratio(N,student_rate,Blue_collar,Housewife):   #학생20% 리스트 
    plist=[]
    """
    if float(student_rate+Blue_collar+Housewife)!=1.0:

        print("input_error")
    else: 
    """
    for i in range(int(N*student_rate)):
        plist.append("Student")#plist.append("StudentWithVacation")
    for i in range(int(N*Blue_collar)):
        plist.append("Blue_collar")
    for i in range(int(N*Housewife)):
        plist.append("Housewife")
    return plist


def human_generate(N,gausmean,seed,plist,memo):
    hlist=[]    
    plist=plist
    random.seed(seed) 
    standard=int(gausmean*N)
    #랜덤리스트 생성
    for _ in range(int(N)):
        val = random.gauss(gausmean,1)
        if val <= 0.5:
            val = 1
        hlist.append(round(val))
    #평균값 맞추기
    if sum(hlist)>standard:                 
        val=sum(hlist)-standard
        for i in range(val):
            dec_mean(hlist,i)
    else:
        val=standard-sum(hlist)
        for i in range(val):
            inc_mean(hlist,i)

    #파일로 저장
    with open("update/{0}_N{1}_seed{2}.txt".format(memo,standard,seed), 'w') as f:  
        family=0
        buildingcount=0
        #fam_per_building=b_percent(random.random())
        fam_per_building=random.normalvariate(4.2045,0.3032131965)
        id=0
        for item in hlist:
            family+=1
            for __ in range(item):
                htype=random.sample(plist,1)[0]
                plist.remove(htype)
               
                if __==item-1:
                    id+=1
                    f.write("%s(%d)\n"% (htype,id))
                else:
                    id+=1
                    f.write("%s(%d)," % (htype,id))
            buildingcount+=1
            if buildingcount >=fam_per_building:
                buildingcount=0
                fam_per_building=random.normalvariate(4.2045,0.3032131965)
                f.write("\n")
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
   

def testcode(student_rate,b_collar_rate,h_wife_rate,trial,memo):
    for i in range(trial):
        plist = population_ratio(100,student_rate,b_collar_rate,h_wife_rate)#plist = population_ratio(10000,student_rate,b_collar_rate,h_wife_rate)
        
        human_generate(37.25,2.6848,i,plist,memo)#human_generate(3725,2.6848,i,plist,memo)
        print('*',end="")
    



#student, bluecollar , housewife
#5:3:2
testcode(0.5, 0.3, 0.2,1,'sbh532')
testcode(0.5, 0.2, 0.3,1,'shb532')
testcode(0.2, 0.5, 0.3,1,'bhs532')
testcode(0.3, 0.5, 0.2,1,'bsh532')
testcode(0.2, 0.3, 0.5,1,'hbs532')
testcode(0.3, 0.2, 0.5,1,'hsb532')
#4:4:2
testcode(0.4, 0.4, 0.2,1,'sbh442')
testcode(0.4, 0.2, 0.4,1,'shb442')
testcode(0.2, 0.4, 0.4,1,'hbs442')


#7:2:1
testcode(0.7, 0.2, 0.1,1,'sbh721')
testcode(0.7, 0.1, 0.2,1,'shb721')
testcode(0.1, 0.7, 0.2,1,'bhs721')
testcode(0.2, 0.7, 0.1,1,'bsh721')
testcode(0.1, 0.2, 0.7,1,'hbs721')
testcode(0.2, 0.1, 0.7,1,'hsb721')





#testcode(0.5,5/20,5/20,1,'studentmain') #student
#testcode(5/20,0.5,5/20,1,'bluecollarmain') #bluecollar
#testcode(5/20,5/20,0.5,1,'housewifemain') #housewife

#random.choice(list)
#print(list)
#원룸 100% -> 학생 2000명 원룸인구 10000명            


#아파트 분포
"""
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

"""
