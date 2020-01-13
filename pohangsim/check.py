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
        
        self.insert_output_port("check_garbagecan")
        self.insert_output_port("gov_report")

        self.human_id_map = {}
        self.human_port_map = {}         
        self.satis_func = satis_func
        self.satisfaction = 100

    def register_human(self, human_id):
        in_p = "before_satisfaction[{0}]".format(human_id)
        out_p = "after_satisfaction[{0}]".format(human_id)
        
        self.human_id_map[human_id] = out_p
        self.human_port_map[in_p] = 0
        
        self.insert_input_port(in_p)
        self.insert_output_port(out_p)
        
        return (in_p, out_p)
        
    def get_human_port_map(self):
        return self.human_map
        
    def ext_trans(self,port, msg):
        if port == self.human_port_map:
            #print('[check]!')
            self._cur_state = "CHECK"
            #value = msg.retrieve()[0]
            
            #print(value)
        if port =="respond":
            #print("[check]%")
            self.satisfaction += self.satis_func(msg.retrieve()[0])
            if self.satisfaction >= 100:
                self.satisfaction = 100
            if self.satisfaction < 0:
                self._cur_state = "REPORT"
        print(self.get_name() + str(self.satisfaction))

    def output(self):
        if self._cur_state=="CHECK":
            #print('[check]@')
            msg = SysMessage(self.get_name(), "check_garbagecan")
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