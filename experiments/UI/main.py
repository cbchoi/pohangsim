import sys
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import *

from main_window import MSWSsimulator

app = QApplication(sys.argv)

ui_file = QFile("../../PohangSim.ui")
loader = QUiLoader()
window = loader.load(ui_file)
ui_file.close()
pohangMSWS = MSWSsimulator(window)
pohangMSWS.show()

sys.exit(app.exec_())
