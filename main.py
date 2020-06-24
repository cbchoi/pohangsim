import sys
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import *

from UI.main_window import MSWSsimulator
def main():

    app = QApplication(sys.argv)

    ui_file = QFile("UI/screen/PohangSim.ui")
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    pohangMSWS = MSWSsimulator(window)
    pohangMSWS.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

