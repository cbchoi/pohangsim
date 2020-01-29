from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

import os
import datetime

from config import *
#from instance.config import *

class Check(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, htype):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("CHECK", 0)
        self.insert_state("REPORT",0)
        
        self.insert_input_port("request")
        self.insert_input_port("checked") # from garbage can
        
        self.insert_output_port("check") # to garbage can
        self.insert_output_port("gov_report")

       
        self.htype = htype
#        self.satis_func = satis_func
#        self.satisfaction = 100
#        self.hid = hid

        
    def ext_trans(self,port, msg):
        if port == "request":
            self._cur_state = "CHECK"
            #value = msg.retrieve()[0]
            
            #print("[check] " + self.get_name() + " CHECK state")
        if port =="checked":
            #print("[check]%"
            self.htype.satisfaction += self.htype.get_satisfaction_func(msg.retrieve()[0])
            if self.htype.satisfaction >= 100:
                self.htype.satisfaction = 100
            if self.htype.satisfaction < 0:
                self.htype.satisfaction += 31
                self.htype._cur_state = "REPORT"
            #print(SystemSimulator().get_engine("sname").get_global_time())
            #print("[check] "+self.get_name() + ":" + str(self.htype.satisfaction))

    def output(self):
        if self._cur_state=="CHECK":
            msg = SysMessage(self.get_name(), "check")
            msg.insert(self.htype)
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
