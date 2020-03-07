from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

import os
import datetime
import random

from config import *
#from instance.config import *

from pohangsim.job import TimeStruct
from pohangsim.job import HumanType

class Human(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, human):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.human= human
        self.init_state("IDLE")
        
        self.insert_state("IDLE", Infinite)
##
        unit_t = self.human.get_out().get_unit_time()
        #print(self.human.get_type(), " out time:", unit_t)
        self.insert_state("WAIT", unit_t)
        #self.insert_state("WAIT", 1)
  
        self.insert_input_port("start")
        self.insert_input_port("end")
        
        self.insert_output_port("trash")  #쓰레기 배출포트?

    def ext_trans(self,port, msg):
        if port == "start":
            self._cur_state = "WAIT"
        if port == "end":
            self._cur_state = "IDLE"
                        
    def output(self):
        if self._cur_state == "WAIT":
            msg = None

            if self.human.get_type() == "Student":
                if random.randint(0, 100) < 25:
                    return None

            msg = SysMessage(self.get_name(), "trash")
            msg.insert(self.human)

            return msg

    def int_trans(self):
        if self._cur_state == "WAIT":
            self._cur_state = "WAIT"
            unit_t = self.human.get_out().get_unit_time()
            #print(self.human.get_type(), " out time:", unit_t)
            self.update_state("WAIT", unit_t)
            #self.update_state("WAIT", 1)
