from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

import os
import datetime

from config import *
from instance.config import *

import math

from core_component import FamilyType
'''
class Family(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, garbage_capacity):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.garbage_capacity=garbage_capacity
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("WAIT", 1)

        self.insert_input_port("start")
        self.insert_input_port("receive")

        self.insert_output_port("retrash")

    def ext_trans(self,port, msg):
        if port=="receive":
            self.data=msg.retrieve()
            self.garbage_capacity=self.garbage_capacity+self.data[0]
            print(self.garbage_capacity)
            if self.garbage_capacity>=30:
                self._cur_state = "WAIT"
            else:
                return None

    def output(self):
        if self._cur_state == "WAIT":
            if self.garbage_capacity>=30:
                self.garbage_capacity=self.garbage_capacity-30
            msg = SysMessage(self.get_name(), "throwaway")
            msg.insert(30)
            return msg

    def int_trans(self):
        if self._cur_state == "WAIT":
            self._cur_state="IDLE"
'''

class Family(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, family_type):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("FLUSH", 0)

        #self.insert_input_port("start")
        self.insert_input_port("receive")
        self.insert_output_port("trash")

        self.family_type = family_type
        
    def ext_trans(self,port, msg):
        if port=="receive":
            data = msg.retrieve()
            
            self.family_type.stack_garbage(data[0])
            #print("!")
            #print(self.family_type.get_stack_amount())
            
            if self.family_type.should_empty():
                if self.family_type.is_flush(data[1]):
                    self._cur_state = "FLUSH"

    def output(self):
        msg = SysMessage(self.get_name(), "trash")
        msg.insert(self.family_type.get_stack_amount())
        #print(self.family_type.get_stack_amount())
        self.family_type.empty_stack()
        
        return msg
            
    def int_trans(self):
        if self._cur_state == "FLUSH":
            self._cur_state = "IDLE"