import math, re
from scenario_editor import *
# Ui
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

	def __init__(self, familytypelist, scenario, _parent=None):
		super(BuildingTypeManager, self).__init__(_parent)
		self.obj = _parent
		self.scenario = scenario
		self.tempscenario=scenario
		self.total_buildingn = 0
		self.total_pagen = 0
		self.currentpage = 1  # 1로 초기화
		self.b_in_page = 0
		# button 동작 정의
		self.next.clicked.connect(self.increase_page)
		self.before.clicked.connect(self.decrease_page)
		self.first.clicked.connect(self.first_page)
		self.last.clicked.connect(self.last_page)
		self.addButton.clicked.connect(self.add_building)
		self.removeButton.clicked.connect(self.remove_buildings)
		self.EditButton.clicked.connect(self.edit_familytype)
		self.AddtoBuilding.clicked.connect(self.put_in)
		#okbutton
		self.buttonBox.accepted.connect(self.update_familytype_list) #also updates scenario
		self.buttonBox.rejected.connect(self.revert_scenario)
		self.update_page()
		self.familydialog = FamilyTypeManager

		self.FamilyTypeList.addItems(self.familytype_list)
		self.familytype_list = familytypelist
		self.load_list()
		#drag and drop
		self.B1.installEventFilter(self)
		self.B2.installEventFilter(self)
		self.B3.installEventFilter(self)
		self.B1_2.installEventFilter(self)
		self.B2_2.installEventFilter(self)
		self.B3_2.installEventFilter(self)

	def eventFilter(self, obj, event):
		if event.type() is QEvent.DragEnter:
			if QApplication.mouseButtons() == Qt.LeftButton:
				event.accept()


		if event.type() == QEvent.Type.Drop:
			if event.mimeData().hasText() and event.mimeData().hasURLs():
				pass
			else:
				if isinstance(obj, QPushButton):
					self.put_in_drop(obj)

		return False
	def put_in_drop(self,obj):
		id = int(re.findall("\d+",obj.text())[0])
		for item in self.FamilyTypeList.selectedItems():
			item = re.findall("\d+", item.text())
			item = list(map(int, item))
			self.tempscenario[id-1].add(FamilyClass(item[0], item[1], item[2], item[3]))
		self.update_page()

	def put_in(self):
		index_start = 6 * (self.currentpage - 1)
		dv = []
		for i in range(self.b_in_page):
			dv.append(self.tempscenario[i + index_start])
		for item in self.FamilyTypeList.selectedItems():
			item = re.findall("\d+",item.text())
			item= list(map(int, item))
			if self.B1.isChecked():
				dv[0].add(FamilyClass(item[0],item[1],item[2],item[3]))
			if self.B2.isChecked():
				dv[1].add(FamilyClass(item[0],item[1],item[2],item[3]))
			if self.B3.isChecked():
				dv[2].add(FamilyClass(item[0],item[1],item[2],item[3]))
			if self.B1_2.isChecked():
				dv[3].add(FamilyClass(item[0],item[1],item[2],item[3]))
			if self.B2_2.isChecked():
				dv[4].add(FamilyClass(item[0],item[1],item[2],item[3]))
			if self.B3_2.isChecked():
				dv[5].add(FamilyClass(item[0],item[1],item[2],item[3]))
		self.update_page()


	def load_list(self):
		for family in self.familytype_list:
			self.FamilyTypeList.addItem(family)
	def revert_scenario(self):
		self.tempscenario = self.scenario
		self.signal.LISTSIG.emit(self.familytype_list)

	def update_familytype_list(self):
		self.scenario = self.tempscenario
		self.signal.LISTSIG.emit(self.familytype_list)

	@Slot()
	def get_familytype_list(self, list):
		while (self.FamilyTypeList.count() > 0):
			self.FamilyTypeList.takeItem(0)
		for family in list:
			self.FamilyTypeList.addItem(family)
		self.familytype_list = list

	def edit_familytype(self):
		ui_file = QFile("../../FamilyDialog.ui")
		loader = QUiLoader()
		self.familydialog = loader.load(ui_file)
		ui_file.close()
		self.familydialog.setModal(True)
		self.familydialog = FamilyTypeManager(self.familytype_list, self.familydialog)
		self.familydialog.OKSIG.connect(self.get_familytype_list)
		self.familydialog.show()


	def add_building(self):
		building = BuildingClass()
		self.tempscenario.add(building)
		if self.b_in_page == 6:
			self.currentpage += 1
			self.update_page()
			if self.currentpage < self.total_pagen:
				self.currentpage = self.total_pagen
		self.update_page()

	def remove_buildings(self):
		index_start = 6 * (self.currentpage - 1)
		dv = []
		for i in range(self.b_in_page):
			dv.append(self.tempscenario[i + index_start])
		if self.B1.isChecked():
			self.tempscenario.remove(dv[0])
			self.B1.setChecked(False)
		if self.B2.isChecked():
			self.tempscenario.remove(dv[1])
			self.B2.setChecked(False)
		if self.B3.isChecked():
			self.tempscenario.remove(dv[2])
			self.B3.setChecked(False)
		if self.B1_2.isChecked():
			self.tempscenario.remove(dv[3])
			self.B1_2.setChecked(False)
		if self.B2_2.isChecked():
			self.tempscenario.remove(dv[4])
			self.B2_2.setChecked(False)
		if self.B3_2.isChecked():
			self.tempscenario.remove(dv[5])
			self.B3_2.setChecked(False)
		self.update_page()
		if self.b_in_page == 6:
			if self.currentpage != 1:
				self.currentpage -= 1
		self.update_page()

	def increase_page(self):
		if self.currentpage < self.total_pagen:
			self.currentpage += 1
			self.update_page()

	def decrease_page(self):
		if self.currentpage > 1:
			self.currentpage -= 1
			self.update_page()

	def first_page(self):
		self.currentpage = 1
		self.update_page()

	def last_page(self):
		self.currentpage = self.total_pagen
		self.update_page()

	def update_page(self):
		self.total_buildingn = len(self.tempscenario)
		self.total_pagen = math.ceil(len(self.tempscenario) / 6)
		if self.currentpage == self.total_pagen:
			self.b_in_page = self.total_buildingn - (6 * (self.total_pagen - 1))
		else:
			self.b_in_page = 6

		showlist = []
		for building in self.tempscenario:
			flist = []
			for family in building:
				flist.append(family)
			showlist.append(flist)
		index_start = 6 * (self.currentpage - 1)
		# print(showlist[index_start:index_start+self.b_in_page])
		self.update_text(index_start, *showlist[index_start:index_start + self.b_in_page])

	def update_text(self, id, B1=False, B2=False, B3=False, B1_2=False, B2_2=False, B3_2=False):
		self.label.setText(str(self.currentpage) + "/" + str(self.total_pagen))
		B1text, B2text, B3text, B1_2text, B2_2text, B3_2text = "", "", "", "", "", ""
		if B1 is not False:
			B1text = "building id =" + str(id + 1) + " \n"
			for family in B1:
				B1text += "S:" + str(family.S) + "H:" + str(family.H) + "B:" + str(family.B) + "familycan size:" + str(
					family.cansize) + "\n"
			self.B1.setText(B1text)
			self.B1.setVisible(True)
			self.B1.setAcceptDrops(True)
		else:
			self.B1.setText("building id =" + str(id + 1) + " \n")
			self.B1.setVisible(False)
		if B2 is not False:
			B2text = "building id =" + str(id + 2) + "\n"
			for family in B2:
				B2text += "S:" + str(family.S) + "H:" + str(family.H) + "B:" + str(family.B) + "familycan size:" + str(
					family.cansize) + "\n"
			self.B2.setText(B2text)
			self.B2.setVisible(True)
		else:
			self.B2.setText("building id =" + str(id + 2) + "\n")
			self.B2.setVisible(False)
		if B3 is not False:
			B3text = "building id =" + str(id + 3) + "\n"
			for family in B3:
				B3text += "S:" + str(family.S) + "H:" + str(family.H) + "B:" + str(family.B) + "familycan size:" + str(
					family.cansize) + "\n"
			self.B3.setText(B3text)
			self.B3.setVisible(True)
		else:
			self.B3.setText("building id =" + str(id + 3) + "\n")
			self.B3.setVisible(False)
		if B1_2 is not False:
			B1_2text = "building id =" + str(id + 4) + " \n"
			for family in B1_2:
				B1_2text += "S:" + str(family.S) + "H:" + str(family.H) + "B:" + str(
					family.B) + "familycan size:" + str(family.cansize) + "\n"
			self.B1_2.setText(B1_2text)
			self.B1_2.setVisible(True)
		else:
			self.B1_2.setText("building id =" + str(id + 4) + " \n")
			self.B1_2.setVisible(False)
		if B2_2 is not False:
			B2_2text = "building id =" + str(id + 5) + "\n"
			for family in B2_2:
				B2_2text += "S:" + str(family.S) + "H:" + str(family.H) + "B:" + str(
					family.B) + "familycan size:" + str(family.cansize) + "\n"
			self.B2_2.setText(B2_2text)
			self.B2_2.setVisible(True)
		else:
			self.B2_2.setText("building id =" + str(id + 5) + "\n")
			self.B2_2.setVisible(False)
		if B3_2 is not False:
			B3_2text = "building id =" + str(id + 6) + "\n"
			for family in B3_2:
				B3text += "S:" + str(family.S) + "H:" + str(family.H) + "B:" + str(family.B) + "familycan size:" + str(
					family.cansize) + "\n"
			self.B3_2.setText(B3_2text)
			self.B3_2.setVisible(True)
		else:
			self.B3_2.setText("building id =" + str(id + 6) + "\n")
			self.B3_2.setVisible(False)

	def __getattr__(self, attr):
		return getattr(self.obj, attr)

	def show(self):
		self.obj.show()
