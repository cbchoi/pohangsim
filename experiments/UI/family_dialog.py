from scenario_editor import *
#ui
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import *
from PySide2.QtGui import *


class FamilyTypeManager(QDialog):
    def __init__(self, _parent=None):
        super(FamilyTypeManager, self).__init__(_parent)
        self.obj = _parent
        self.increaseS.pressed.connect()
        self.increaseH.pressed.connect()
        self.increaseB.pressed.connect()
        self.increaseFCan.pressed.connect()
        self.decreaseS.pressed.connect()
        self.decreaseH.pressed.connect()
        self.decreaseB.pressed.connect()
        self.decreaseFCan.pressed.connect()

    def decrease_value(self,target):
        if target.value<=0:
            pass
        else:
            target.value-=1
    def increase_value(self,target):
        target.value-=1
    def __getattr__(self, attr):
        return getattr(self.obj, attr)

    def show(self):
        self.obj.show()
