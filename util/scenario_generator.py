import contexts

#FamilyType and humantype
from pohangsim.core_component import HumanType
#from pohangsim.core_component import FamilyType

#job class load
from pohangsim.job import *

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
		self.family_id-=1

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
		self.familylist=[]
		self.N_family=0
		pass

	def add(self,obj):
		self.familylist.append(obj)
		self.N_family+=1

	def __del__(self):
		self.building_id-=1

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
class ScenarioType(object):
	scenario_id=0
	N_building=0
	buildinglist=[]
	def __new__(self):
		self.scenario_id+=1
		return object.__new__(self)
		pass
	def __init__(self):
		self.scenario_id=self.scenario_id
		self.N_building=0
		self.buildinglist=[]
		pass

	def add(self,obj):
		self.buildinglist.append(obj)
		self.N_building+=1

	def __del__(self):
		self.scenario_id-=1

	def __repr__(self):
		repr=""
		for k in self.buildinglist:
			for j in k:
				for i in j:
					repr+=str(i.get_type())+" "
				repr+="\n"
			repr+="\n"
		#return repr
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

#builindg2= BuildingType(2000) # 아파트
building1= BuildingType(50) # 공동주택
building1.add(FamilyType(1,0,0,5))
building1.add(FamilyType(0,1,0,5))
building1.add(FamilyType(0,0,1,5))
building1.add(FamilyType(1,1,1,5))
building1.add(FamilyType(2,1,1,5))

#print("building repr\n",building1)
#print("building member list\n",building1.familylist)
scenario=ScenarioType()
scenario.add(building1)
scenario.add(building1)
#print(scenario.buildinglist)


for building in scenario:
	for family in building:
		for member in family:
			pass
			#print(member)
		#print(family)
	#print(building)

def scenario_generator(BuildingN,FamilyN,StudentN,HomemakerN,WorkerN,cansize=[],memo="a"):
	familyperbuilding=BuildingN/FamilyN
	student_in_family=StudentN/FamilyN
	Homemaker_in_family=HomemakerN/FamilyN
	Worker_in_family=WorkerN/FamilyN
	Scenario=ScenarioType()

	for budiling in range(BuildingN):
		building=BuildingType(cansize[building])
	#BuildingNumber is given
	#Family per Building can be derived from FamilyNumber
