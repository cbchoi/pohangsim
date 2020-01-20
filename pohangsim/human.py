from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

import os
import datetime

from config import *
#from instance.config import *

from job import TimeStruct
from job import HumanType

class Human(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, human):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.human= human
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("WAIT", self.human.get_out().get_unit_time())
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
            #print("[human] " + self.get_name())
            msg = SysMessage(self.get_name(), "trash")
            msg.insert(self.human.get_trash())
            msg.insert(self.human.get_id())
            return msg

    def int_trans(self):
        if self._cur_state == "WAIT":
            self._cur_state = "WAIT"
            self.update_state("WAIT", self.human.get_out().get_unit_time())
            #self.update_state("WAIT", 1)
