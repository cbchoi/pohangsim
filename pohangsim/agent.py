import contexts
import sys

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
from job import Student
from job import Housewife
from job import Blue_collar
from job import White_collar
from job import Inoccupation
from job import Self_employment

from human import Human
from check import Check
from government import Government
from garbagecan import GarbageCan
from family import Family


se = SystemSimulator()

SystemSimulator().register_engine("sname", SIMULATION_MODE)

c = Clock(0, 40, "clock", "sname")
SystemSimulator().get_engine("sname").register_entity(c)

g = GarbageCan(0, 40, "gc", 'sname', 10)
SystemSimulator().get_engine("sname").register_entity(g)

h_id=-27
mod = sys.modules[__name__]

def get_human_id():
    global h_id
    h_id += 1
    return h_id


#hlist1  = [Self_employment(0),Self_employment(1)]
hlist2  = [Self_employment(1),Self_employment(2),Student(3)]
#hlist3  = [Student(get_human_id()),Student(get_human_id())]
#hlist4  = [Student(get_human_id())]
hlist5  = [Housewife(4),Blue_collar(5),Inoccupation(6),Student(7)]
#hlist6  = [White_collar(get_human_id()),White_collar(get_human_id()),Inoccupation(get_human_id())]
#hlist7  = [Blue_collar(get_human_id()),Blue_collar(get_human_id()),Blue_collar(get_human_id())]
#hlist8  = [Blue_collar(get_human_id()),Blue_collar(get_human_id()),Blue_collar(get_human_id())]
#hlist9  = [AFF(get_human_id()),Inoccupation(get_human_id()),Housewife(get_human_id())]
#hlist10 = [White_collar(get_human_id()),White_collar(get_human_id()),Housewife(get_human_id())]

ftype1 = FamilyType(20)
ftype2 = FamilyType(15)
f1 = Family(0, 40,"family",'sname', ftype1)
f2 = Family(0, 40,"family",'sname', ftype2)

gv = Government(0, 40,"government","sname")
SystemSimulator().get_engine("sname").register_entity(gv)

#Family Register

for htype in hlist2:
    #hid = get_human_id()
    name = htype.get_name()
    cname = "check[{0}]".format(htype.get_name())
    ch = Check(0, 40, name, "sname", htype.get_satisfaction_func, htype.get_id())
    h1 = Human(0, 40, cname, "sname", htype)

    SystemSimulator().get_engine("sname").register_entity(h1)
    SystemSimulator().get_engine("sname").register_entity(ch)
    #f1.register_member(htype)
    ftype1.register_member(htype)
    
    ports = g.register_human(htype.get_id())
    SystemSimulator().get_engine("sname").coupling_relation(h1, "trash", ch, "request")
    SystemSimulator().get_engine("sname").coupling_relation(ch, "check", g, ports[0])

    SystemSimulator().get_engine("sname").coupling_relation(g, ports[1], ch, "checked")
    SystemSimulator().get_engine("sname").coupling_relation(ch, "gov_report", gv, "recv_report")
    
    SystemSimulator().get_engine("sname").coupling_relation(None, "start", h1, "start")
    SystemSimulator().get_engine("sname").coupling_relation(None, "end", h1, "end")
    SystemSimulator().get_engine("sname").coupling_relation(h1, "trash", f1, "receive_membertrash")
    
    #SystemSimulator().get_engine("sname").coupling_relation(h1, "trash", g, "recv")

for htype in hlist5:
    name = htype.get_name()
    cname = "check[{0}]".format(htype.get_name())
    
    ch = Check(0, 40, cname, "sname", htype.get_satisfaction_func,htype.get_id())

    h1 = Human(0, 40, name, "sname", htype)
    SystemSimulator().get_engine("sname").register_entity(h1)
    SystemSimulator().get_engine("sname").register_entity(ch)
    
    #f1.register_member(htype)
    ftype2.register_member(htype)
    
    ports = g.register_human(htype.get_id())
    SystemSimulator().get_engine("sname").coupling_relation(h1, "trash", ch, "request")
    SystemSimulator().get_engine("sname").coupling_relation(ch, "check", g, ports[0])

    SystemSimulator().get_engine("sname").coupling_relation(g, ports[1], ch, "checked")
    SystemSimulator().get_engine("sname").coupling_relation(ch, "gov_report", gv, "recv_report")
    
    SystemSimulator().get_engine("sname").coupling_relation(None, "start", h1, "start")
    SystemSimulator().get_engine("sname").coupling_relation(None, "end", h1, "end")
    SystemSimulator().get_engine("sname").coupling_relation(h1, "trash", f1, "receive_membertrash")
    
    #SystemSimulator().get_engine("sname").coupling_relation(h1, "trash", g, "recv")      
    
SystemSimulator().get_engine("sname").register_entity(f1)
SystemSimulator().get_engine("sname").coupling_relation(f1, "takeout_trash", g, "recv_garbage")
SystemSimulator().get_engine("sname").register_entity(f2)
SystemSimulator().get_engine("sname").coupling_relation(f2, "takeout_trash", g, "recv_garbage")

SystemSimulator().get_engine("sname").insert_input_port("start")


SystemSimulator().get_engine("sname").coupling_relation(None, "start", c, "start")
SystemSimulator().get_engine("sname").coupling_relation(None, "end", c, "end")

#SystemSimulator().get_engine("sname").insert_external_event("report", None)

SystemSimulator().get_engine("sname").insert_external_event("start", None)
SystemSimulator().get_engine("sname").simulate()


