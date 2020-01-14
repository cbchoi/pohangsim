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
#from job import Student
#from job import Housewife
from human import Human
from check import Check
from government import Government
from garbagecan import GarbageCan
from family import Family

se = SystemSimulator()

SystemSimulator().register_engine("sname", SIMULATION_MODE)

c = Clock(0, 26, "clock", "sname")
SystemSimulator().get_engine("sname").register_entity(c)

g = GarbageCan(0, 26, "gc", 'sname', 10)
SystemSimulator().get_engine("sname").register_entity(g)

h_id = 0

def get_human_id():
    global h_id
    h_id += 1
    return h_id
    
hlist = [AFF(get_human_id()), AFF(get_human_id()), AFF(get_human_id())]
#htype2 = HumanType(Student.get_type(), Student.get_wakeup_time(), Student.get_sleep_time(), Student.get_out_time(), Student.get_in_time(), Student.get_trash())
#htype3 = HumanType(Housewife.get_type(), Housewife.get_wakeup_time(), Housewife.get_sleep_time(), Housewife.get_out_time(), Housewife.get_in_time(), Housewife.get_trash())

ftype = FamilyType(30)
f1 = Family(0, 26,"family",'sname', ftype)

gv = Government(0,26,"government","sname")
SystemSimulator().get_engine("sname").register_entity(gv)

#Family Register
for htype in hlist:
    hid = htype.get_id()
    name = "aff[{0}]".format(hid)
    cname = "check[{0}]".format(hid)
    
    ch = Check(0, 26, cname, "sname", htype.get_satisfaction_func)
    h1 = Human(0, 26, name, "sname", htype)
    SystemSimulator().get_engine("sname").register_entity(h1)
    SystemSimulator().get_engine("sname").register_entity(ch)
    
    #f1.register_member(htype)
    ftype.register_member(htype)
    
    SystemSimulator().get_engine("sname").coupling_relation(h1, "trash", ch, "request")
    SystemSimulator().get_engine("sname").coupling_relation(ch, "check", g, "check")
    SystemSimulator().get_engine("sname").coupling_relation(g, "respond", ch, "checked")
    SystemSimulator().get_engine("sname").coupling_relation(ch, "gov_report", gv, "gov_report")
    
    SystemSimulator().get_engine("sname").coupling_relation(None, "start", h1, "start")
    SystemSimulator().get_engine("sname").coupling_relation(None, "end", h1, "end")
    SystemSimulator().get_engine("sname").coupling_relation(h1, "trash", f1, "receive")
    
    #SystemSimulator().get_engine("sname").coupling_relation(h1, "trash", g, "recv")

SystemSimulator().get_engine("sname").register_entity(f1)
SystemSimulator().get_engine("sname").coupling_relation(f1, "trash", g, "recv")

SystemSimulator().get_engine("sname").insert_input_port("start")


SystemSimulator().get_engine("sname").coupling_relation(None, "start", c, "start")
SystemSimulator().get_engine("sname").coupling_relation(None, "end", c, "end")

#SystemSimulator().get_engine("sname").insert_external_event("report", None)

SystemSimulator().get_engine("sname").insert_external_event("start", None)
SystemSimulator().get_engine("sname").simulate()


