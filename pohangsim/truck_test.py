import contexts

from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

from config import *
from instance.config import *

from clock import Clock
from core_component import HumanType
from core_component import FamilyType
from job import AFF

from government import Government

from human import Human
from check import Check
from garbagecan import GarbageCan
from garbage_truck import GarbageTruck
from family import Family

# Human ID Handling
h_id = 0

def get_human_id():
    global h_id
    h_id += 1
    return h_id
    
se = SystemSimulator()

# Manage Simulation Engine's External Port
SystemSimulator().register_engine("sname", SIMULATION_MODE)
SystemSimulator().get_engine("sname").insert_input_port("start")

c = Clock(0, 100, "clock", "sname")
SystemSimulator().get_engine("sname").register_entity(c)

g = GarbageCan(0, 100, "garbage_can", 'sname', 10)
SystemSimulator().get_engine("sname").register_entity(g)

gt = GarbageTruck(0, 100, "garbage_truck", 'sname', 10, [(0, 1)])
SystemSimulator().get_engine("sname").register_entity(gt)
    
hlist = [AFF(get_human_id()), AFF(get_human_id()), AFF(get_human_id())]

ftype = FamilyType(30)
f1 = Family(0, 100,"family",'sname', ftype)

gv = Government(0, 100,"government","sname")
SystemSimulator().get_engine("sname").register_entity(gv)

#Family Register
for htype in hlist:
    hid = htype.get_id()
    name = "aff[{0}]".format(hid)
    cname = "check[{0}]".format(hid)
    
    ch = Check(0, 100, cname, "sname", htype.get_satisfaction_func)
    h1 = Human(0, 100, name, "sname", htype)
    SystemSimulator().get_engine("sname").register_entity(h1)
    SystemSimulator().get_engine("sname").register_entity(ch)
    
    #f1.register_member(htype)
    ftype.register_member(htype)
    
    SystemSimulator().get_engine("sname").coupling_relation(h1, "trash", ch, "request")
    SystemSimulator().get_engine("sname").coupling_relation(ch, "check_garbagecan", g, "check_garbage")
    SystemSimulator().get_engine("sname").coupling_relation(g, "res_check", ch, "checked")
    SystemSimulator().get_engine("sname").coupling_relation(ch, "gov_report", gv, "recv_report")
    
    SystemSimulator().get_engine("sname").coupling_relation(None, "start", h1, "start")
    SystemSimulator().get_engine("sname").coupling_relation(None, "end", h1, "end")
    SystemSimulator().get_engine("sname").coupling_relation(h1, "trash", f1, "receive_membertrash")
    
    #SystemSimulator().get_engine("sname").coupling_relation(h1, "trash", g, "recv")

SystemSimulator().get_engine("sname").register_entity(f1)
SystemSimulator().get_engine("sname").coupling_relation(f1, "takeout_trash", g, "recv_garbage")

SystemSimulator().get_engine("sname").coupling_relation(None, "start", c, "start")
SystemSimulator().get_engine("sname").coupling_relation(None, "end", c, "end")

SystemSimulator().get_engine("sname").coupling_relation(None, "start", gt, "start")
SystemSimulator().get_engine("sname").coupling_relation(None, "end", gt, "end")

# Connect Truck & Can
ports = gt.register_garbage_can(0)
SystemSimulator().get_engine("sname").coupling_relation(g, "res_garbage", gt, ports[0])
SystemSimulator().get_engine("sname").coupling_relation(gt, ports[1], g, "req_empty")

SystemSimulator().get_engine("sname").insert_external_event("start", None)
SystemSimulator().get_engine("sname").simulate()


