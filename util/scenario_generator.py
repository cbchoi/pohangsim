import contexts

#FamilyType and humantype
from pohangsim.core_component import HumanType
#from pohangsim.core_component import FamilyType

#job class load
from pohangsim.job import *


class Scenario(object):
    def __init__(self):
        pass
        #self.buildings
        #self.student
        #self.homemaker
        #self.construction_worker





class FamilyType(Student,Homemaker,Blue_collar):
    family_id=0
    N_member=0
    memberlist=[]
    def __new__(self, S,H,B,cansize) :
        self.family_id+=1
        fam=[]
        for i in range(S):
            self.N_member+=1
            fam.append(Student(HumanType(self.N_member)))
        for i in range(H):
            self.N_member+=1
            fam.append(Homemaker(HumanType(self.N_member)))
        for i in range(B):
            self.N_member+=1
            fam.append(Blue_collar(HumanType(self.N_member)))
        self.memberlist.append(fam)
        return object.__new__(self)

    def __init__(self,S,H,B,cansize):
        self.cansize=cansize
        self.memberlist=[]
        self.family_id=self.family_id
        self.N_member=0
        for i in range(S):
            self.N_member+=1
            self.memberlist.append(Student(HumanType(self.N_member)))
        for i in range(H):
            self.N_member+=1
            self.memberlist.append(Homemaker(HumanType(self.N_member)))
        for i in range(B):
            self.N_member+=1
            self.memberlist.append(Blue_collar(HumanType(self.N_member)))

    def __add__(self,member):
        self.memberlist.append(member)
        self.N_member+=1
    def __del__(self):
        self.family_id-=1

    def __repr__(self):
        repr=""
        for i in self.memberlist:
            repr+=str(i.get_type())+","
        return repr
    def __len__(self):
        return len(self.memberlist)


    def __iter__(self):
        self.index = 0
        return self
 
    def __next__(self):
        if self.index >= len(self):
            raise StopIteration
 
        n = self.memberlist[self.index]
        self.index += 1
        return n

class BuildingType(object):
    building_id=0
    N_family=0
    familylist=[]
    def __new__(self,cansize):
        self.building_id+=1
        return object.__new__(self)
        pass
    def __init__(self,cansize):
        self.building_id=self.building_id
        self.garbagecan_size=cansize
        pass

    def add(self,obj):
        self.familylist.append(obj)
        self.N_family+=1

    def __del__(self):
        self.building_id-=1

    def __repr__(self):
        repr=""
        for j in self.familylist:
            repr+="\n"
            for i in j:
                repr+=str(i.get_type())+" "
        return repr

#builindg2= BuildingType(2000) # 아파트
building1= BuildingType(50) # 공동주택

building1.add(FamilyType(0,1,0,5))
building1.add(FamilyType(0,0,1,5))
building1.add(FamilyType(1,1,1,5))
building1.add(FamilyType(2,1,1,5))

print(building1)
print(building1.building_id)
building1= BuildingType(50) # 공동주택

building1.add(FamilyType(0,1,0,5))
building1.add(FamilyType(0,0,1,5))
building1.add(FamilyType(1,1,1,5))
building1.add(FamilyType(2,1,1,5))

print(building1)
print(building1.building_id)

