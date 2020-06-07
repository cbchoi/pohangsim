import sys
import contexts
import dill

#FamilyType and humantype
from pohangsim.core_component import HumanType
#from pohangsim.core_component import FamilyType
#job class load
from pohangsim.job import *

class FamilyClass(Student,Homemaker,Blue_collar):
	id=0
	N_member=0
	memberlist=[]

	def __getnewargs__(self):
		return self.S, self.H, self.B, self.cansize
	def __new__(self, S,H,B,cansize) :
		self.id+=1
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
		self.S=S
		self.H=H
		self.B=B
		self.cansize=cansize
		self.memberlist=[]
		self.id=self.id
		self.N_member=0
		if S>0:
			for i in range(S):
				self.N_member+=1
				self.memberlist.append(Student(HumanType(self.N_member)))
		if H>0:
			for i in range(H):
				self.N_member+=1
				self.memberlist.append(Homemaker(HumanType(self.N_member)))
		if B>0:
			for i in range(B):
				self.N_member+=1
				self.memberlist.append(Blue_collar(HumanType(self.N_member)))

	def __add__(self,member):
		self.memberlist.append(member)
		self.N_member+=1
	def __del__(self):
		self.id-=1

	def __repr__(self):
		repr =str(self.memberlist)
		return repr
	def __len__(self):
		return len(self.memberlist)
	def __getitem__(self, key):
		return self.memberlist[key]

	def __iter__(self):
		self.index = 0
		return self
 
	def __next__(self):
		if self.index >= len(self):
			raise StopIteration
 
		n = self.memberlist[self.index]
		self.index += 1
		return n

class BuildingClass(object):
	id=0
	N_family=0
	familylist=[]
	def __new__(self,cansize=50):
		self.id+=1
		
		return object.__new__(self)
		pass
	def __init__(self,cansize=50):
		self.id=self.id
		self.garbagecan_size=cansize
		self.familylist=[]
		self.N_family=0
		pass

	def add(self,obj):
		self.familylist.append(obj)
		self.N_family+=1

	def remove(self,obj):
		self.familylist.remove(obj)
		self.N_family-=1

	def __del__(self):
		self.id-=1

	def __repr__(self):
		repr=str(self.familylist)
		return repr
	def __len__(self):
		return len(self.familylist)
	def __getitem__(self, key):
		return self.familylist[key]

	def __iter__(self):
		self.index = 0
		return self
 
	def __next__(self):
		if self.index >= len(self):
			raise StopIteration
 
		n = self.familylist[self.index]
		self.index += 1
		return n

class ScenarioClass(object):
	id=0
	N_building=0
	buildinglist=[]
	memo=""
	def __new__(self):
		self.id+=1
		return object.__new__(self)
		pass
	def __init__(self):
		self.id=self.id
		self.N_building=0
		self.buildinglist=[]
		self.memo=""
		pass

	def add(self,obj):
		self.buildinglist.append(obj)
		self.N_building+=1

	def __del__(self):
		self.id-=1

	def __repr__(self):
		return str(self.buildinglist)

	def __len__(self):
		return len(self.buildinglist)

	def __iter__(self):
		self.index = 0
		return self
 
	def __next__(self):
		if self.index >= len(self):
			raise StopIteration
 
		n = self.buildinglist[self.index]
		self.index += 1
		return n
	def __getitem__(self, key):
		return self.buildinglist[key]

	def remove(self,obj):
		self.buildinglist.remove(obj)
		self.N_building-=1


#N개의 빌딩을 가진  시나리오 class를 생성

def new_scenario_GUI(N):
	scenario=ScenarioClass()
	for idx in range(N):
		scenario.add(BuildingClass())
	#print(scenario.id)
	"""
	if len(cansize)==1:
		for idx in range(N):
			scenario.add(BuildingClass(cansize[0]))
	else:
		if len(cansize)!=N:
			raise ValueError
		else:
			for idx in range(N):
				scenario.add(BuildingClass(cansize[idx]))
	"""
	return scenario
def load_scenario_GUI(filename):
	file=open(filename,"rb")
	scenario=dill.load(file)
	file.close()
	return scenario

def save_scenario_GUI(scenario,familytype,output):
	file=open(output[0]+".scn","wb")
	dill.dump((scenario,familytype),file)
	file.close()


#편집할 빌딩 선택 input=scenario
def select_building_GUI(scenario):
	id=int(input("select id {0}\n".format(list(range(len(scenario))))))
	
	edit_building_GUI(scenario,id)
	
def edit_family_GUI(building,id,S,H,B,familycan):
	building(add)
	Tempcansize=input("tem can size")
	add_family_GUI(scenario,id,S,H,B,Tempcansize)
	pass
	#S,H,B,tempcan=value from ui
	#addbutton.clicked.connect(add_family)

#building 에 family추가
def add_family_GUI(scenario,id,S,H,B,tempcan):
	scenario[id].add(FamilyClass(S,H,B,tempcan))
	#print(scenario[id])
	#print(scenario[id][0].cansize)
def remove_family_GUI(scenario,id,familyid):
	scenario[id].remove(scenario[id].familylist[familyid])

#
"""
scenario=new_scenario_GUI(0)
building1= BuildingClass(50) # 공동주택

building1.add(FamilyClass(1,0,0,5))
building1.add(FamilyClass(0,1,0,5))
building1.add(FamilyClass(0,0,1,5))

scenario.add(building1)

save_scenario_GUI(scenario,"savetest.txt")

#
#a=load_scenario_GUI("savetest.txt")

#print(a.__dict__.items())
#print(a.memo)

#select_building_GUI(scenariolist[0])
#print(scenariolist[0])
#print(scenariolist[0][0])
scenariolist=[] #scenariolist[scenariosclass[buildingclass[familyclass[]]]]
scenariolist.append(new_scenario_GUI(0)) #빌딩이 0개인 시나리오를 시나리오 리스트에 추가
building1= BuildingClass(50) # 공동주택
building1.add(FamilyClass(1,0,0,5))
building1.add(FamilyClass(0,1,0,5))
building1.add(FamilyClass(0,0,1,5))
building1.add(FamilyClass(1,1,1,5))
building1.add(FamilyClass(2,1,1,5))
#print(scenariolist)
#print(scenariolist[0])
scenariolist[0].add(building1)
#save_scenario_GUI(scenariolist,0,"")
scenariolist.append(load_scenario_GUI("C:/research/web/pohangsim/util/scenario.txt"))
pprint(scenariolist)

#builindg2= BuildingClass(2000) # 아파트
#building1=BuildingClass(100)
building1= BuildingClass(50) # 공동주택
building1.add(FamilyClass(1,0,0,5))
building1.add(FamilyClass(0,1,0,5))
building1.add(FamilyClass(0,0,1,5))
building1.add(FamilyClass(1,1,1,5))
building1.add(FamilyClass(2,1,1,5))


"""


