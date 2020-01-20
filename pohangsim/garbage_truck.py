from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

from config import *
from instance.config import *

class GarbageTruck(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, storage, schedule):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("INITAL_APPROACH", 5)
        self.insert_state("REQUEST", 0)
        self.insert_state("APPROACH", 24)

        self.insert_input_port("start")
        self.insert_input_port("end")
        
        self.garbage_id_map = {}
        self.garbage_port_map = {}
        self.truck_storage = storage
        self.truck_current_storage = 0
        
        # for analysis
        self.accummulated_garbage = 0
        
        self.schedule = schedule
        # schedule = [(current_can_id, next_can_delay)]
        self.cur_index = 0

    def register_garbage_can(self, garbage_can_id):
        in_p = "trash_from_can[{0}]".format(garbage_can_id)
        out_p = "empty_can[{0}]".format(garbage_can_id)
        #print ('[truck_id]',garbage_can_id)
        
        self.garbage_id_map[garbage_can_id] = out_p
        self.garbage_port_map[in_p] = 0
        
        self.insert_input_port(in_p)
        self.insert_output_port(out_p)
        
        return (in_p, out_p)
        
    def get_garbage_can_port_map(self):
        return self.garbage_map
        
    def ext_trans(self, port, msg):
        #print(port)    
        if port == "start":
            self._cur_state = "INITAL_APPROACH"
        elif port == "end":
            self._cur_state = "IDLE"
        elif port in self.garbage_port_map:
            self.garbage_port_map[port] += msg.retrieve()[0] # 각 건물별 쓰레기 수거량 분석
            self.truck_current_storage += msg.retrieve()[0]
            #print("[truck_storage]"+  str(port) + ":" +str(self.garbage_port_map[port]),self.truck_current_storage)
            
    def output(self):
        if self._cur_state == "REQUEST":
            msg = SysMessage(self.get_name(), self.garbage_id_map[self.schedule[self.cur_index][0]])
            msg.insert(-1)
            return msg
        return None

    def int_trans(self):
        if self._cur_state == "INITAL_APPROACH":
            self._cur_state = "REQUEST"
        elif self._cur_state == "REQUEST":
            if self.cur_index < len(self.schedule)-1:
                self.cur_index += 1
                self._cur_state = "REQUEST"
                next_can_delay = self.schedule[self.cur_index][1]
                self.update_state(self._cur_state, next_can_delay)
            else:
                self._cur_state = "APPROACH"
        elif self._cur_state == "APPROACH":
            self.cur_index = 0
            self.accummulated_garbage += self.truck_current_storage
            #print ('[truck_end]',self.truck_current_storage)
            self.truck_current_storage = 0
            self._cur_state = "REQUEST"

    def __del__(self):
        print(self.accummulated_garbage)