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
        #self.setFixedSize(600,200)# not working
        print(self.size())

    def __getattr__(self, attr):
        return getattr(self.obj, attr)

    def show(self):
        self.obj.show()
