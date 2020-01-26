from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

import sys
import os
import datetime

from config import *
#from instance.config import *

class GarbageCan(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, size):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", 0)
        self.insert_state("PROC_TRUCK", 0)
        
        #checker port
        #self.insert_output_port("res_check") #checker에게 garbage 값 리턴
        #self.insert_input_port("check_garbage") #checker 에게  garbage 비율 요청 메세지를 받는 포트
        
        #trash input from family
        self.insert_input_port("recv_garbage")  #family가 garbage 배출할때 받는 포트
        
        #garbage truck port
        self.insert_input_port("req_empty")   #garbage_truck에서 입력받는 포트
        self.insert_output_port("res_garbage")  # garbgage_truck output port
        
        self.can_size = size
        self.cur_amount = 0

        self.req_empty_amount = 0

        self.human_id_map = {}
        self.human_port_map = {} 

        self.family_id_map = {}
        self.family_port_map = {} 

        self.recv_checker_port = []
        self.name=name
        self.dlist={}
        self.fileout=open("can_output{0}.csv".format(self.name) ,"w")
    
    def __del__(self):

        for ag_key, ag_value in self.dlist.items():
            cur_list = list(ag_value.keys())
            print(cur_list)
            length = cur_list[-1]
            indx = 0

            for i in range(length):
                if i == cur_list[indx]:
                    print(ag_value[cur_list[indx]])
                    indx += 1

                self.fileout.write(str(i))
                self.fileout.write(",")
                self.fileout.write(str(ag_key))
                self.fileout.write(",")
                
                for item in ag_value[cur_list[indx]]:
                    self.fileout.write(str(item))
                    self.fileout.write(",")
                
                self.fileout.write("\n")
                        
        self.fileout.close()



    def register_human(self, human_id):
        #checker port
        in_p = "check_trash[{0}]".format(human_id)
        out_p = "check_trash[{0}]".format(human_id)
        
        self.human_id_map[human_id] = out_p
        self.human_port_map[in_p] = out_p
        
        self.insert_input_port(in_p)
        self.insert_output_port(out_p)
        
        return (in_p, out_p)

    def get_human_port_map(self):
        return self.human_map

    def register_family(self, family_id):
        #checker port
        #print ("[fam_id]",family_id)
        in_p = "trash_from_family[{0}]".format(family_id)
        out_p = "trash[{0}]".format(family_id)
        
        self.family_id_map[family_id] = out_p
        self.family_port_map[in_p] = out_p
        
        self.insert_input_port(in_p)
        self.insert_output_port(out_p)
        
        return (in_p, out_p)

    def get_family_port_map(self):
        return self.family_map        

    def ext_trans(self, port, msg):
        if port in self.human_port_map:     #garbage 비율  Process
            #print('[check]1')
            self._cur_state = "PROCESS"
            self.recv_checker_port.append(port)

        if port in self.family_port_map:       #garbage 누적
            #print("fam_port",port)
            data = msg.retrieve()

            ev_t = SystemSimulator().get_engine("sname").get_global_time()
            ag_id = 0
            ag_name = ""
            ag_amount = 0
            ag_satisfaction = 0

            for member, accumulated in data[0].items():
                self.cur_amount += accumulated
                ag_id - member.get_id()
                ag_name = member.get_name()
                ag_amount = accumulated
                ag_satisfaction = member.get_satisfaction()
                #print(SystemSimulator().get_engine("sname").get_global_time())
                
                if ag_name not in self.dlist:
                    self.dlist[ag_name] = {}

                self.dlist[ag_name][ev_t] = (ag_amount, ag_satisfaction) 
                print(self.dlist[ag_name])

            
        if port == "req_empty":  #garbage 양 반환 process
            #print("[truck]1")
            self.req_empty_amount = msg.retrieve()[0]
            self._cur_state = "PROC_TRUCK"

    def output(self):
        if self._cur_state == "PROCESS":  
            #print('[check]$')
            #print(self.human_port_map[self.recv_checker_port])
            port = self.recv_checker_port.pop(0)
            msg = SysMessage(self.get_name(), self.human_port_map[port])
            msg.insert(float(self.cur_amount/self.can_size))
            #print("$")
            #print("[gc] " + str(float(self.cur_amount/self.can_size)))
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
            if len(self.recv_checker_port) > 0:
                self._cur_state = "PROCESS"
            else:
                self._cur_state = "IDLE"
        elif self._cur_state == "PROC_TRUCK":
            self._cur_state = "IDLE"
