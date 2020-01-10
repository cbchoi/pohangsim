import contexts

from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

from crawler import Crawler

from config import *
from instance.config import *

se = SystemSimulator()

SystemSimulator().register_engine("sname", SIMULATION_MODE)

a = Crawler(0, Infinite, "Peter", "sname")

SystemSimulator().get_engine("sname").insert_input_port("start")
SystemSimulator().get_engine("sname").insert_input_port("report")
SystemSimulator().get_engine("sname").register_entity(a)

SystemSimulator().get_engine("sname").coupling_relation(None, "report", a, "report")
SystemSimulator().get_engine("sname").insert_external_event("report", None)
SystemSimulator().get_engine("sname").simulate()


