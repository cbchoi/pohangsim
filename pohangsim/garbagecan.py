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
        self.insert_state("PROC_TRUCK", 0)
        
        #checker port
        self.insert_output_port("res_check") #checker에게 garbage 값 리턴
        self.insert_input_port("check_garbage") #checker 에게  garbage 비율 요청 메세지를 받는 포트
        
        #trash input from family
        self.insert_input_port("recv_garbage")  #family가 garbage 배출할때 받는 포트
        
        #garbage truck port
        self.insert_input_port("req_empty")   #garbage_truck에서 입력받는 포트
        self.insert_output_port("res_garbage")  # garbgage_truck output port
        
        self.can_size = size
        self.cur_amount = 0

        self.req_empty_amount = 0

    def ext_trans(self, port, msg):
        if port == "check_garbage":     #garbage 비율  Process
            #print('[check]1')
            self._cur_state = "PROCESS"
        if port == "recv_garbage":       #garbage 누적
            data = msg.retrieve()
            self.cur_amount += data[0]
            #print("[fam]1", self.cur_amount)
            
        if port == "req_empty":  #garbage 양 반환 process
            #print("[truck]1")
            self.req_empty_amount = msg.retrieve()[0]
            self._cur_state = "PROC_TRUCK"

    def output(self):
        if self._cur_state == "PROCESS":  
            #print('[check]$')
            msg = SysMessage(self.get_name(), "res_check")
            msg.insert(float(self.cur_amount/self.can_size))
            return msg
        if self._cur_state == "PROC_TRUCK":
            #print("!@@")
            if self.req_empty_amount < 0:
                self.req_empty_amount = self.cur_amount
            self.cur_amount -= self.req_empty_amount
            msg = SysMessage(self.get_name(), "res_garbage")
            msg.insert(self.req_empty_amount)
            return msg
            
        return None

    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"
        elif self._cur_state == "PROC_TRUCK":
            self._cur_state = "IDLE"