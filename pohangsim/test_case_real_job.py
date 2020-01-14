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
from garbage_truck import GarbageTruck
from family import Family


se = SystemSimulator()

SystemSimulator().register_engine("sname", SIMULATION_MODE)

c = Clock(0, 100, "clock", "sname")
SystemSimulator().get_engine("sname").register_entity(c)

g = GarbageCan(0, 100, "gc", 'sname', 10)
SystemSimulator().get_engine("sname").register_entity(g)

gt = GarbageTruck(0, 100, "garbage_truck", 'sname', 10, [(0, 1)])
SystemSimulator().get_engine("sname").register_entity(gt)

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



gv = Government(0, 100,"government","sname")
SystemSimulator().get_engine("sname").register_entity(gv)
i=0
#Family Register
for flist in hlist:
    i+=1
    ftype = FamilyType(len(flist)*3)
    f = Family(0, 100,"family",'sname', ftype)
    for htype in flist:
        #hid = get_human_id()
        name = htype.get_name()
        cname = "check[{0}]".format(htype.get_name())
        ch = Check(0, 100, name, "sname", htype.get_satisfaction_func, htype.get_id())
        h1 = Human(0, 100, cname, "sname", htype)

        SystemSimulator().get_engine("sname").register_entity(h1)
        SystemSimulator().get_engine("sname").register_entity(ch)
        #f1.register_member(htype)
        ftype.register_member(htype)
    
        ports = g.register_human(htype.get_id())
        SystemSimulator().get_engine("sname").coupling_relation(h1, "trash", ch, "request")
        SystemSimulator().get_engine("sname").coupling_relation(ch, "check", g, ports[0])

        SystemSimulator().get_engine("sname").coupling_relation(g, ports[1], ch, "checked")
        SystemSimulator().get_engine("sname").coupling_relation(ch, "gov_report", gv, "recv_report")
    
        SystemSimulator().get_engine("sname").coupling_relation(None, "start", h1, "start")
        SystemSimulator().get_engine("sname").coupling_relation(None, "end", h1, "end")
        SystemSimulator().get_engine("sname").coupling_relation(h1, "trash", f, "receive_membertrash")
    
        #SystemSimulator().get_engine("sname").coupling_relation(h1, "trash", g, "recv")
    SystemSimulator().get_engine("sname").register_entity(f)
    SystemSimulator().get_engine("sname").coupling_relation(f, "takeout_trash", g, "recv_garbage")

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