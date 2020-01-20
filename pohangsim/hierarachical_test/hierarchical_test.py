import contexts
import sys

from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

from config import *

from clock import Clock

se = SystemSimulator()

SystemSimulator().register_engine("sname", SIMULATION_MODE)
SystemSimulator().get_engine("sname").insert_input_port("start")
SystemSimulator().get_engine("sname").insert_input_port("end")

c = Clock(0, 26, "clock", "sname")

SystemSimulator().get_engine("sname").register_entity(c)
SystemSimulator().get_engine("sname").coupling_relation(None, "start", c, "start")
SystemSimulator().get_engine("sname").insert_external_event("start", None)
SystemSimulator().get_engine("sname").simulate()
