from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

import os
import datetime

from config import *
from instance.config import *

class YourClassName(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", REQUEST_FREQ)

        self.insert_input_port("report")


    def ext_trans(self,port, msg):
        if port == "report":
            self._cur_state = "PROCESS"
            

    def output(self):
        if self._cur_state == "PROCESS":
            pass
            
        return None

    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "PROCESS"