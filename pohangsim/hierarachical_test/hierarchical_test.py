import contexts
import sys

from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

from config import *

from clock import Clock

from evsim.structural_model import StructuralModel

class HT01(StructuralModel):
    def __init__(self, instance_time, destroy_time, name, engine_name):
        super(HT01, self).__init__(name)
        
        self.set_name(name)
        self.insert_input_port("start")
        self.insert_input_port("end")

        self.insert_output_port("out")

        c = Clock(instance_time, destroy_time, "clock", engine_name)
        self.insert_model(c)

        self.insert_external_input_coupling("start", c, "start")
        self.insert_external_input_coupling("end", c, "end")
        self.insert_external_output_coupling(c, "out", "out")
        pass

class HT02(StructuralModel):
    def __init__(self, instance_time, destroy_time, name, engine_name):
        super(HT02, self).__init__(name)

        self.set_name(name)
        self.insert_input_port("start")
        self.insert_input_port("end")

        self.insert_output_port("out")

        c = HT01(instance_time, destroy_time, "HT01", engine_name)
        c2 = Clock(instance_time, destroy_time, "clock", engine_name)

        self.insert_model(c)
        self.insert_model(c2)
        self.insert_external_input_coupling("start", c, "start")
        self.insert_external_input_coupling("end", c, "end")
        
        self.insert_internal_coupling(c, "out", c2, "start")
        self.insert_external_output_coupling(c2, "out", "out")
        pass

se = SystemSimulator()

SystemSimulator().register_engine("sname", SIMULATION_MODE, TIME_DENSITY)
SystemSimulator().get_engine("sname").insert_input_port("start")
SystemSimulator().get_engine("sname").insert_input_port("end")
SystemSimulator().get_engine("sname").insert_output_port("out")

c = HT02(0, 26, "ht02", "sname")

SystemSimulator().get_engine("sname").register_entity(c)
SystemSimulator().get_engine("sname").coupling_relation(None, "start", c, "start")
SystemSimulator().get_engine("sname").coupling_relation(c, "out", None, "out")
SystemSimulator().get_engine("sname").insert_external_event("start", None)
SystemSimulator().get_engine("sname").simulate()
print(SystemSimulator().get_engine("sname").get_generated_event())