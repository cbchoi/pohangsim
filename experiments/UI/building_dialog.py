import math
from scenario_editor import *
#Ui
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import *
from PySide2.QtGui import *


from family_dialog import FamilyTypeManager
class FSig(QObject):
	LISTSIG = Signal(list)
	def __init__(self):
		QObject.__init__(self)


class BuildingTypeManager(QDialog):
	signal = FSig()
	familytype_list = []
	def __init__(self,familytypelist, scenario, _parent = None):
		super(BuildingTypeManager, self).__init__(_parent)
		self.obj = _parent
		self.scenario=scenario
		self.total_buildingn=0
		self.total_pagen = 0
		self.currentpage=1 #1로 초기화
		self.b_in_page = 0
		#button 동작 정의
		self.next.clicked.connect(self.increase_page)
		self.before.clicked.connect(self.decrease_page)
		self.first.clicked.connect(self.first_page)
		self.last.clicked.connect(self.last_page)
		self.addButton.clicked.connect(self.add_building)
		self.removeButton.clicked.connect(self.remove_buildings)
		self.EditButton.clicked.connect(self.edit_familytype)
		self.update_page()
		self.familydialog=FamilyTypeManager
		self.buttonBox.accepted.connect(self.update_familytype_list)
		self.FamilyTypeList.addItems(self.familytype_list)
		self.familytype_list=familytypelist
		self.templist=[]
		self.load_list()
		self.B1.setAcceptDrops(True)
		self.B2.setAcceptDrops(True)
		self.B3.setAcceptDrops(True)
		self.B1_2.setAcceptDrops(True)
		self.B2_2.setAcceptDrops(True)
		self.B3_2.setAcceptDrops(True)

	#familytype drag and drop
	def dragEnterEvent(self, e):
		e.accept()
		"""
		if e.mimeData().hasFormat('text/plain'):
			e.accept()
		else:
			e.ignore()
		"""
	def dropEvent(self, e):
		print(self.text)
		pass
		#self.

	def load_list(self):
		for index in self.familytype_list:
			self.FamilyTypeList.addItem(
				"S:" + str(index.S) + "H:" + str(index.H) + "B:" + str(index.B) + "_" + str(index.cansize))

	def update_familytype_list(self):
		self.familytype_list=self.templist
		self.signal.LISTSIG.emit(self.familytype_list)

	@Slot()
	def get_familytype_list(self,list):
		while (self.FamilyTypeList.count() > 0):
			self.FamilyTypeList.takeItem(0)
		for family in list:
			self.FamilyTypeList.addItem(
				"S:" + str(family.S) + "H:" + str(family.H) + "B:" + str(family.B) + "_" + str(family.cansize))
		self.templist = list

	def edit_familytype(self):
		ui_file = QFile("../../FamilyDialog2.ui")
		loader = QUiLoader()
		self.familydialog = loader.load(ui_file)
		ui_file.close()
		self.familydialog.setModal(True)
		self.familydialog = FamilyTypeManager(self.familytype_list, self.familydialog)
		self.familydialog.OKSIG.connect(self.get_familytype_list)
		self.familydialog.show()

	def add_family_to_building(self,text,building_id,family):
		text=text.split('_')
		print(text)
		#self.scenario[building_id].add(FamilyClass(int(self.editS_2.toPlainText()), int(self.editH_2.toPlainText()), int(self.editB_2.toPlainText()), int(self.editFCan_2.toPlainText())))

		self.update_page()

	def add_building(self):
		building=BuildingClass()
		self.scenario.add(building)
		if self.b_in_page==6:
			self.currentpage+=1
			self.update_page()
			if self.currentpage<self.total_pagen:
				self.currentpage=self.total_pagen
		self.update_page()

	def remove_buildings(self):
		index_start = 6 * (self.currentpage - 1)
		dv=[]
		for i in range(self.b_in_page):
			dv.append(self.scenario[i+index_start])
		if self.B1.isChecked():
			self.scenario.remove(dv[0])
			self.B1.setChecked(False)
		if self.B2.isChecked():
			self.scenario.remove(dv[1])
			self.B2.setChecked(False)
		if self.B3.isChecked():
			self.scenario.remove(dv[2])
			self.B3.setChecked(False)
		if self.B1_2.isChecked():
			self.scenario.remove(dv[3])
			self.B1_2.setChecked(False)
		if self.B2_2.isChecked():
			self.scenario.remove(dv[4])
			self.B2_2.setChecked(False)
		if self.B3_2.isChecked():
			self.scenario.remove(dv[5])
			self.B3_2.setChecked(False)
		self.update_page()
		if self.b_in_page == 6:
			if self.currentpage !=1:
				self.currentpage -= 1
		self.update_page()
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
		self.total_buildingn = len(self.scenario)
		self.total_pagen = math.ceil(len(self.scenario) / 6)
		if self.currentpage==self.total_pagen:
			self.b_in_page=self.total_buildingn-(6*(self.total_pagen-1))
		else:
			self.b_in_page=6
		
		showlist=[]
		for building in self.scenario:
			flist=[]
			for family in building:
				flist.append(family)
			showlist.append(flist)
		index_start =6*(self.currentpage-1)
		#print(showlist[index_start:index_start+self.b_in_page])
		self.update_text(index_start,*showlist[index_start:index_start+self.b_in_page])
	def update_text(self,id,B1=False,B2=False,B3=False,B1_2=False,B2_2=False,B3_2=False):
		self.label.setText(str(self.currentpage)+"/"+str(self.total_pagen))
		B1text,B2text,B3text,B1_2text,B2_2text,B3_2text="","","","","",""
		if B1 is not False:
			B1text="building id ="+str(id+1)+" \n"
			for family in B1:
				B1text+="S:"+str(family.S)+"H:"+str(family.H)+"B:"+str(family.B)+"familycan size:"+str(family.cansize)+"\n"
			self.B1.setText(B1text)
			self.B1.setVisible(True)
		else:
			self.B1.setVisible(False)
		if B2 is not False:
			B2text = "building id =" + str(id+2) + "\n"
			for family in B2:
				B2text+="S:"+str(family.S)+"H:"+str(family.H)+"B:"+str(family.B)+"familycan size:"+str(family.cansize)+"\n"
			self.B2.setText(B2text)
			self.B2.setVisible(True)
		else:
			self.B2.setVisible(False)
		if B3 is not False:
			B3text = "building id =" + str(id+3) + "\n"
			for family in B3:
				B3text+="S:"+str(family.S)+"H:"+str(family.H)+"B:"+str(family.B)+"familycan size:"+str(family.cansize)+"\n"
			self.B3.setText(B3text)
			self.B3.setVisible(True)
		else:
			self.B3.setVisible(False)
		if B1_2 is not False:
			B1_2text="building id ="+str(id+4)+" \n"
			for family in B1_2:
				B1_2text+="S:"+str(family.S)+"H:"+str(family.H)+"B:"+str(family.B)+"familycan size:"+str(family.cansize)+"\n"
			self.B1_2.setText(B1_2text)
			self.B1_2.setVisible(True)
		else:
			self.B1_2.setVisible(False)
		if B2_2 is not False:
			B2_2text = "building id =" + str(id+5) + "\n"
			for family in B2_2:
				B2_2text+="S:"+str(family.S)+"H:"+str(family.H)+"B:"+str(family.B)+"familycan size:"+str(family.cansize)+"\n"
			self.B2_2.setText(B2_2text)
			self.B2_2.setVisible(True)
		else:
			self.B2_2.setVisible(False)
		if B3_2 is not False:
			B3_2text = "building id =" + str(id+6) + "\n"
			for family in B3_2:
				B3text+="S:"+str(family.S)+"H:"+str(family.H)+"B:"+str(family.B)+"familycan size:"+str(family.cansize)+"\n"
			self.B3_2.setText(B3_2text)
			self.B3_2.setVisible(True)
		else:
			self.B3_2.setVisible(False)

	def __getattr__(self, attr):
		return getattr(self.obj, attr)

	def show(self):
		self.obj.show()
