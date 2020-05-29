from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import *
from PySide2.QtGui import *

class GenericWorker(QObject):
    start = SIGNAL(type)
    def __init__(self, function, *args, **kwargs):
        super(GenericWorker, self).__init__()

        self.function = function
        self.args = args
        self.kwargs = kwargs

    @Slot()
    def run(self, some_string_arg):
        self.function(*self.args, **self.kwargs)

my_thread = QThread()
my_thread.start()

# This causes my_worker.run() to eventually execute in my_thread:
my_worker = GenericWorker(...)
my_worker.moveToThread(my_thread)
my_worker.start.connect(my_worker.run) #  <---- Like this instead
my_worker.start.emit("hello")