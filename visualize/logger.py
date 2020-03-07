import sys
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import rcParams

import time
import numpy as np

class MyWindow(object):
    def __init__(self, parent):
        self.obj = parent
        self.obj.addTxt.clicked.connect(self.addTxt)
        central = self.obj.centralWidget()
        
        self._main = QWidget()
        self.obj.setCentralWidget(self._main)

        left = QWidget()
        right = QWidget()

        container = QHBoxLayout(self._main)
        container.addWidget(left)
        container.addWidget(right)

        llayout = QVBoxLayout(left)
        llayout.addWidget(self.obj.addTxt)
        llayout.addWidget(self.obj.txtList)
        
        layout = QVBoxLayout(right)
        

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(static_canvas)
        self.obj.addToolBar(NavigationToolbar(static_canvas, self.obj))

        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)
        self.obj.addToolBar(Qt.BottomToolBarArea,NavigationToolbar(dynamic_canvas, self.obj))

        self._static_ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), ".")

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._timer = dynamic_canvas.new_timer(100, [(self._update_canvas, (), {})])
        self._timer.start()

    def addTxt(self):
        self.obj.txtList.addItem("!")

    def show(self):
        self.obj.show()

    def _update_canvas(self):
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._dynamic_ax.figure.canvas.draw()

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    ui_file = QFile("logger.ui")
    loader = QUiLoader()
    window = loader.load(ui_file)
    print(type(window))
    ui_file.close()

    my_window = MyWindow(window)
    #a = WindowClass()
    #window.addTxt.clicked.connect(addTxt)

    my_window.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()


    