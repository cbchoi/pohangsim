from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.definition import *
from evsim.system_message import SysMessage

import sys

class Human(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, human):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.human= human
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        unit_t = self.human.get_out().get_unit_time()
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
            #print("[human] " + self.get_name(), self.human.get_trash(),SystemSimulator().get_engine("sname").get_global_time(),file=sys.__stdout__)
            msg = SysMessage(self.get_name(), "trash")
            msg.insert(self.human)

            return msg

    def int_trans(self):
        if self._cur_state == "WAIT":
            self._cur_state = "WAIT"
            unit_t = self.human.get_out().get_unit_time()
            #if self.human.get_type() == "Student":
            #    print(unit_t)
            self.update_state("WAIT", unit_t)
            #self.update_state("WAIT", 1)
