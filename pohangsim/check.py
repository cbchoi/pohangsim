from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

import os
import datetime

from config import *
from instance.config import *

class Check(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, satis_func):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("CHECK", 0)
        self.insert_state("REPORT", 0)
        
        self.insert_input_port("request")
        self.insert_input_port("checked")
        
        self.insert_output_port("check")
        self.insert_output_port("gov_report")
        
        self.satis_func = satis_func
        self.satisfaction = 100

    def ext_trans(self,port, msg):
        if port == "request":
            #print('[check]!')
            self._cur_state = "CHECK"
            
        if port =="checked":
            #print("[check]%")
            value = msg.retrieve()[0]
            
            #print(value)
            self.satisfaction += self.satis_func(value)
            if self.satisfaction >= 100:
                self.satisfaction = 100
            
            #print(self.satisfaction)
            if self.satisfaction < 0:
                self._cur_state = "REPORT"

    def output(self):
        if self._cur_state=="CHECK":
            #print('[check]@')
            msg = SysMessage(self.get_name(), "check")
            return msg
            
        if self._cur_state == "REPORT":
            #print('[check]#')
            msg = SysMessage(self.get_name(), "gov_report")
            return msg
            
        return None

    def int_trans(self):
        if self._cur_state == "CHECK":
            self._cur_state = "IDLE"
        elif self._cur_state=="REPORT":
            self._cur_state = "IDLE"