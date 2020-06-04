from PySide2.QtWidgets import *
from scenario_editor import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile,QTimer, QObject, Slot, Signal, Qt
from PySide2.QtGui import *

class FamilyTypeManager(QDialog):
    def __init__(self, _parent=None):
        super(FamilyTypeManager, self).__init__(_parent)
        self.obj = _parent
        self.timer=QTimer()
        self.addFamilyType.clicked.connect(self.timerstart)

    def timerstart(self):
        self.timer.timeout.connect(self.size)
        self.timer.start(1000)

    def size(self):
        print(self.size())

    def __getattr__(self, attr):
        return getattr(self.obj, attr)

    def show(self):
        self.obj.show()
