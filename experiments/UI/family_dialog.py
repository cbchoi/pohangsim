from scenario_editor import *
#ui
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import *
from PySide2.QtGui import *

import functools

class FamilyTypeManager(QDialog):
    OKSIG=Signal(list)
    def __init__(self,familytypelist, _parent=None):
        super(FamilyTypeManager, self).__init__(_parent)
        self.obj = _parent
        self.editS_2.setPlainText("0")
        self.editH_2.setPlainText("0")
        self.editB_2.setPlainText("0")
        self.editFCan_2.setPlainText("0")
        increaseS=functools.partial(self.increase, self.editS_2)
        increaseH = functools.partial(self.increase, self.editH_2)
        increaseB = functools.partial(self.increase, self.editB_2)
        increaseFCan = functools.partial(self.increase, self.editFCan_2)
        decreaseS = functools.partial(self.decrease, self.editS_2)
        decreaseH = functools.partial(self.decrease, self.editH_2)
        decreaseB = functools.partial(self.decrease, self.editB_2)
        decreaseFCan = functools.partial(self.decrease, self.editFCan_2)
        self.increaseS_2.pressed.connect(increaseS)
        self.increaseH_2.pressed.connect(increaseH)
        self.increaseB_2.pressed.connect(increaseB)
        self.increaseFCan_2.pressed.connect(increaseFCan)
        self.decreaseS_2.pressed.connect(decreaseS)
        self.decreaseH_2.pressed.connect(decreaseH)
        self.decreaseB_2.pressed.connect(decreaseB)
        self.decreaseFCan_2.pressed.connect(decreaseFCan)
        self.addFamilyType_2.clicked.connect(self.add_family)
        self.deleteFamilyType_2.clicked.connect(self.delete_family)
        self.buttonBox.accepted.connect(self.sendlist)
        self.familytype_list=familytypelist
        self.load_list()

    def load_list(self):
        for index in self.familytype_list:
            self.FamilyTypeList_2.addItem("S:"+str(index.S)+ "H:"+str(index.H)+ "B:"+str(index.B)+"_"+ str(index.cansize))


    def sendlist(self):
        self.OKSIG.emit(self.familytype_list)

    def add_family(self):
        family=FamilyClass(int(self.editS_2.toPlainText()), int(self.editH_2.toPlainText()), int(self.editB_2.toPlainText()), int(self.editFCan_2.toPlainText()))
        self.FamilyTypeList_2.addItem("S:"+str(family.S)+ "_H:"+str(family.H)+ "_B:"+str(family.B)+"_"+ str(family.cansize))
        self.familytype_list.append(family)


    def delete_family(self):
        listItems = self.FamilyTypeList_2.selectedItems()
        if not listItems: return
        for item in listItems:
            self.FamilyTypeList_2.takeItem(self.FamilyTypeList_2.row(item))
            del self.familytype_list[self.FamilyTypeList_2.row(item)]
            #del_scenario_GUI(self.scenariolist[self.listWidget.row(item)])

    def decrease(self,obj):
        if int(obj.toPlainText())<=0:
            pass
        else:
            obj.setText(str(int(obj.toPlainText())-1))
    def increase(self,obj):
        obj.setText(str(int(obj.toPlainText())+1))
    """  
    
    def decrease_S(self):
        if int(self.editS.toPlainText())<=0:
            pass
        else:
            self.editS.setText(str(int(self.editS.toPlainText())-1))
    def decrease_H(self):
        if int(self.editH.toPlainText())<=0:
            pass
        else:
            self.editH.setText(str(int(self.editH.toPlainText())-1))
    def decrease_B(self):
        if int(self.editB.toPlainText())<=0:
            pass
        else:
            self.editB.setText(str(int(self.editB.toPlainText())-1))
    def decrease_FC(self):
        if int(self.editFCan.toPlainText())<=0:
            pass
        else:
            self.editS.setText(str(int(self.editS.toPlainText())-1))
    def increase_S(self):
        self.editS.setText(str(int(self.editS.toPlainText())+1))
    def increase_H(self):
        self.editS.setText(str(int(self.editS.toPlainText())+1))
    def increase_B(self):
        self.editS.setText(str(int(self.editS.toPlainText())+1))
    def increase_FC(self):
        self.editS.setText(str(int(self.editS.toPlainText())+1))
    """
    def __getattr__(self, attr):
        return getattr(self.obj, attr)

    def show(self):
        self.obj.show()
