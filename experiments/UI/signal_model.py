from contexts import *
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.definition import *
from PySide2.QtCore import Signal, QObject

class SignalLoop(BehaviorModelExecutor, QObject):
    LOOPBACK_SIG = Signal()
    def __init__(self, instance_time, destruct_time, name, engine_name):
        QObject.__init__(self)
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("IDLE")
        self.insert_state("LOOP", 0)
        self.insert_input_port("start")
    def ext_trans(self, port, msg):
        if port == "start":
            self._cur_state = "LOOP"


    def output(self):
        if self._cur_state == "LOOP":
            print("model is working")
            self.LOOPBACK_SIG.emit()

    def int_trans(self):
        if self._cur_state == "LOOP":
            self._cur_state = "IDLE"