import sys
import os
import time

from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QObject, QTimer, Slot, Signal, QCoreApplication, Qt
from PySide2.QtGui import *


from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np

class DataGroupHandler(QObject):
	DATA_SIG = Signal(list)

	def __init__(self, _parent=None):
		super(DataGroupHandler, self).__init__(_parent)
		self.obj = _parent
		self.editX.setText('0')
		self.editY.setText('0')
		
		self._data_points = []
		pass


	def addBtn(self):
		self._data_points.append((int(self.editX.text()), int(self.editY.text())))
		self.listWidget.addItem("({0}, {1})".format(self._data_points[-1][0], self._data_points[-1][1]))
		self.DATA_SIG.emit(self._data_points)

	def clearBtn(self):
		self._data_points = []

	def __getattr__(self, attr):
		return getattr(self.obj, attr)

class resultWidget(QWidget):
	def __init__(self, _parent = None):
		super(resultWidget, self).__init__(_parent)
		self.obj = _parent

		self.dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
		self.resultLayout.addWidget(self.dynamic_canvas)

		self._dynamic_ax = self.dynamic_canvas.figure.subplots()
		self._data_controller = DataGroupHandler(_parent)

		self.addDataBtn.clicked.connect(self._data_controller.addBtn)

		self._data_controller.DATA_SIG.connect(self._update_canvas)
		self.radioPlot.setChecked(True)
		self.radioPlot.toggled.connect(self._redraw_graph)
		self.radioPie.toggled.connect(self._redraw_graph)
		self.radioBar.toggled.connect(self._redraw_graph)

	def __getattr__(self, attr):
		return getattr(self.obj, attr)

	def show(self):
		self.obj.show()

	@Slot(list)
	def _update_canvas(self, points):
		self._dynamic_ax.clear()
		unzipped = list(zip(*points))
		print("update", *unzipped)
		
		self.x_data, self.y_data = unzipped[0], unzipped[1]
		
		if self.radioPlot.isChecked():
			self._dynamic_ax.plot(unzipped[0], unzipped[1])
		elif self.radioPie.isChecked():
			self._dynamic_ax.pie(upzipped[1]) 
		else:
			self._dynamic_ax.bar(unzipped[0], unzipped[1])

		self.dynamic_canvas.figure.canvas.draw()
		self.obj.repaint()

	@Slot()
	def _redraw_graph(self):
		self._dynamic_ax.clear()
		if self.radioPlot.isChecked():
			self._dynamic_ax.plot(self.x_data, self.y_data)
		elif self.radioPie.isChecked():
			self._dynamic_ax.pie(self.y_data) 
		else:
			self._dynamic_ax.bar(self.x_data, self.y_data)

		self.dynamic_canvas.figure.canvas.draw()
		self.obj.repaint()

		pass
"""		

QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
# Create a Qt application
app = QApplication(sys.argv)

ui_file = QFile("project3.ui")
loader = QUiLoader()
window = loader.load(ui_file)
ui_file.close()

matplot = MatplotlibExample(window)
#smp.show()
matplot.show()
# Enter Qt application main loop
sys.exit(app.exec_())
"""