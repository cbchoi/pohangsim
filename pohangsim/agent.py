import contexts
import sys

from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

from config import *
#from instance.config import *

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


def get_human_id():
    global h_id
    h_id += 1
    return h_id

hlist=[]
fam=[]
file = open('human.txt','r')
lines = file.readlines()
file.close()
for i in range(len(lines)):    
    line=lines[i].split('\n')[0]
    elements=(line.split(','))
    for j in elements:
        fam.append(eval(j))
    hlist.append(fam)
    fam=[]

ftype1 = FamilyType(20)
ftype2 = FamilyType(15)

f1 = Family(0, 40,"family",'sname', ftype1)
f2 = Family(0, 40,"family",'sname', ftype2)

gv = Government(0, 40,"government","sname")
SystemSimulator().get_engine("sname").register_entity(gv)

#Family Register
print(type(Self_employment(1)))
for htype in hlist[1]:
    #hid = get_human_id()
    name = htype.get_name()
    cname = "check[{0}]".format(htype.get_name())
    ch = Check(0, 40, name, "sname", htype.get_satisfaction_func, htype.get_id())
    h1 = Human(0, 40, cname, "sname", htype)
    print( cname)

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

for htype in hlist[3]:
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
SystemSimulator().get_engine("sname").coupling_relation(None, "start", gt, "start")
SystemSimulator().get_engine("sname").coupling_relation(None, "end", gt, "end")

# Connect Truck & Can
ports = gt.register_garbage_can(0)
SystemSimulator().get_engine("sname").coupling_relation(g, "res_garbage", gt, ports[0])
SystemSimulator().get_engine("sname").coupling_relation(gt, ports[1], g, "req_empty")

SystemSimulator().get_engine("sname").insert_external_event("start", None)
SystemSimulator().get_engine("sname").simulate()


