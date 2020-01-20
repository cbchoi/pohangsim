from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

from config import *
from instance.config import *

class GarbageTruck(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("CHECK", 0)

        self.garbage_map = {}

    def register_garbage_can(self, garbage_can_id):
        in_p = "trash_from_can[{0}]".format(garbage_can_id)
        out_p = "empty_can[{0}]".format(garbage_can_id)
        
        self.garbage_map[in_p] = out_p
        
        self.insert_input_port(in_p)
        self.insert_output_port(out_p)
        
    def get_garbage_can_port_map(self):
        return self.garbage_map
        
    def ext_trans(self, port, msg):
        if port in self.garba

    def output(self):
        if self._cur_state=="CHECK":
            print('@')
            msg = SysMessage(self.get_name(), "check")
            return msg
            
        if self._cur_state == "REPORT":
            print('#')
            msg = SysMessage(self.get_name(), "gov_report")
            return msg
            
        return None

    def int_trans(self):
        if self._cur_state == "CHECK":
            self._cur_state = "IDLE"
        elif self._cur_state=="REPORT":
            self._cur_state = "IDLE"