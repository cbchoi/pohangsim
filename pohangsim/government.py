from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

import os
import datetime

from config import *
#from instance.config import *

class Government(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", 0)

        self.insert_input_port("recv_report")  #민원 발생시 받는 포트
        self.reported = {}


    def ext_trans(self,port, msg):
        if port == "recv_report":
            #self._cur_state = "PROCESS"
            member=msg.retrieve()[0]
            if member.get_type() in self.reported:
                self.reported[member.get_type()] += 1
            else:
                self.reported[member.get_type()] = 1

    def __del__(self):
        output_str = ""
        for k, v in self.reported.items():
            output_str += f"{k},{v},"#f"{k}:{v},"
        print(output_str)

    def output(self):
            
        return None

    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"