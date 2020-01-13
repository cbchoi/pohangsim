from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

import os
import datetime

from config import *
from instance.config import *

class GarbageCan(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, size):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", 0)
        
        self.insert_output_port("respond")
        
        
        self.insert_input_port("check")
        self.insert_input_port("recv")
        
        
        
        self.can_size = size
        self.cur_amount = 0


    def ext_trans(self, port, msg):
        if port == "check":
            #print('[check]#')
            self._cur_state = "PROCESS"
        if port =="recv":
            data = msg.retrieve()
            self.cur_amount += data[0]
            print("[fam]!", self.cur_amount)

    def output(self):
        if self._cur_state == "PROCESS":
            #print('[check]$')
            msg = SysMessage(self.get_name(), "respond")
            msg.insert(float(self.cur_amount/self.can_size))
            return msg
            
        return None

    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"