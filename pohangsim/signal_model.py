from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *
from PySide2.QtCore import Signal, QObject

class Fsignal(QObject):
    LOOPBACK_SIG = Signal()
    def __init__(self):
        QObject.__init__(self)
    def send_signal(self):
        self.LOOPBACK_SIG.emit()

class SignalLoop(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("IDLE")
        self.insert_state("FINISH", 0)
        self.insert_input_port("start")
        self.signal=Fsignal()
    def ext_trans(self, port, msg):
        print("signalloop ext")
        if port == "start":
            self._cur_state = "FINISH"
            self.signal.send_signal()

    def output(self):
        if self._cur_state == "FINISH":
            print("model is working")

    def int_trans(self):
        if self._cur_state == "FINISH":
            self._cur_state = "IDLE"