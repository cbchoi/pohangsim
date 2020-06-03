from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *
from PySide2.QtCore import Signal, QObject

class Fsignal(QObject):
    LOOPBACK_SIG = Signal()
    def __init__(self):
        QObject.__init__(self)

class SignalLoop(BehaviorModelExecutor):
    signal = Fsignal()
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("FINISH", Infinite)
        self.insert_input_port("start")
    def ext_trans(self, port, msg):
        #print("signalloop ext")
        if port == "start":
            self._cur_state = "FINISH"
            print("signalloop curstate = finsh")

    def output(self):
        print(SystemSimulator().get_engine("sname").get_global_time())
        #if self.get_destruct_time() == SystemSimulator().get_engine("sname").get_global_time():
        self.signal.LOOPBACK_SIG.emit()

    def int_trans(self):
        #print("signalloop int")
        if self._cur_state == "FINISH":
            self._cur_state = "IDLE"