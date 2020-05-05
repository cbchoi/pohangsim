import contexts

#familytype and humantype
from pohangsim.core_component import HumanType
from pohangsim.core_component import FamilyType

#job class load
from pohangsim.job import *

print("hello")
class Scenario(object):
	def __init__(self):
		self.buildings
		self.student
		self.homemaker
		self.construction_worker

class Building(Student,Homemaker,Blue_collar,S,H,B):
	def __init__(self):
		for _id in range(S):
			Student(HumanType.__init__(self,_id)).__init__(self,b_id)


class Building(Student,Homemaker,Blue_collar,S,H,B):
    buidling_id=0
    def __init__(self, _id, size):
        self.b_id = buidling_id
        self.family_id= 0
        
        self.garbagecan_size = 50
    	Stduent(HumanType.__init__(self,_id))