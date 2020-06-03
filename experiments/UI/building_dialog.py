import math
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QObject, Slot, Signal, Qt
from PySide2.QtGui import *

class BuildingTypeManager(QDialog):
	def __init__(self, scenario, _parent = None):
		super(BuildingTypeManager, self).__init__(_parent)
		self.obj = _parent
		self.scenario=scenario
		self.total_buildingn=len(scenario)
		self.total_pagen = math.ceil(len(scenario)/6)
		self.currentpage=1 #1로 초기화
		self.next.clicked.connect(self.increase_page)
		self.before.clicked.connect(self.decrease_page)
		self.first.clicked.connect(self.first_page)
		self.last.clicked.connect(self.last_page)
		self.update_page()
		print(scenario)
	def increase_page(self):
		if self.currentpage<self.total_pagen:
			self.currentpage+=1
			self.update_page()
	def decrease_page(self):
		if self.currentpage>1:
			self.currentpage-=1
			self.update_page()
	def first_page(self):
		self.currentpage=1
		self.update_page()
	def last_page(self):
		self.currentpage=self.total_pagen
		self.update_page()

	def update_page(self):
		if self.currentpage==self.total_pagen:
			self.b_in_page=self.total_buildingn-(6*(self.total_pagen-1))
		else:
			self.b_in_page=6
		showlist=[]
		for i in range(6):
			if i<self.b_in_page:
				index=i+1+6*(self.currentpage-1)
				if index<self.total_pagen:
					showlist.append(self.scenario[index])
				else:
					showlist.append("")
			else:
				showlist.append("")
		self.update_text(*showlist)
		print(showlist,"showlist" )
	def update_text(self,B1,B2,B3,B1_2,B2_2,B3_2):
		self.label.setText(str(self.currentpage)+"/"+str(self.total_pagen))
		self.B1.setText(B1)
		self.B2.setText(B2)
		self.B3.setText(B3)
		self.B1_2.setText(B1_2)
		self.B2_2.setText(B2_2)
		self.B3_2.setText(B3_2)
 


	def __getattr__(self, attr):
		return getattr(self.obj, attr)

	def show(self):
		self.obj.show()
