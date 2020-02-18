import contexts
import sys
#import numpy as np

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
from job import StudentWithVacation

from human import Human
from check import Check
from government import Government
from garbagecan import GarbageCan
from garbage_truck import GarbageTruck
from family import Family
#simulation_time=448
simulation_time=2192 #quarter
#simulation_time=8762 # year
#simulation_time=26282# 3year
#simulation_time=43802# 5year
#simulation_time=87602# 10year

blist=[]
hlist=[]
fam=[]

#file = open('half.txt','r')
file = open('update/population_s100_N99_seed0.txt','r')
lines = file.readlines()
file.close()
for i in range(len(lines)):  
    line = lines[i].split('\n')[0]
    if not line == "": #빈칸이 아닐경우
        elements = (line.split(','))
        for j in elements: #패밀리 안의 멤버=j
            fam.append(eval(j)) #j를 fam추가
        hlist.append(fam) #fam을 hlist에 추가
        fam=[]    
    else:
        blist.append(hlist)
        hlist = []
    if i == len(lines)-1:
        blist.append(hlist)

se = SystemSimulator()

SystemSimulator().register_engine("sname", SIMULATION_MODE, TIME_DENSITY)

c = Clock(0, simulation_time, "clock", "sname")
SystemSimulator().get_engine("sname").register_entity(c)
gt = GarbageTruck(0, simulation_time, "garbage_truck", 'sname', 68, [e for e in enumerate([0.1 for building in blist])],"7am_only_s0.4")#4.7*13*3
SystemSimulator().get_engine("sname").register_entity(gt)

gv = Government(0, simulation_time,"government","sname")
SystemSimulator().get_engine("sname").register_entity(gv)

def get_human_id():
    global h_id
    h_id += 1
    return h_id

def get_garbagecan_id():
    global garbagecan_id
    garbagecan_id += 1
    return garbagecan_id


#Building Register

i=0
j=0
for building in blist:


    g = GarbageCan(0, simulation_time, "gc[{0}]".format(i), 'sname', 55,"7am_only_s0.4")
    SystemSimulator().get_engine("sname").register_entity(g)
    
    for flist in building:
        ftype = FamilyType(5)
        f = Family(0, simulation_time,"family",'sname', ftype)
        for htype in flist:
            #hid = get_human_id()
            name = htype.get_name()
            cname = "check[{0}]".format(htype.get_name())               
            h1 = Human(0, simulation_time, cname, "sname", htype)
            ch = Check(0, simulation_time, name, "sname", htype)

            SystemSimulator().get_engine("sname").register_entity(h1)
            SystemSimulator().get_engine("sname").register_entity(ch)
            #f1.register_member(htype)
            ftype.register_member(htype)
            
            # Connect Check & Can
            ports = g.register_human(htype.get_id())
            SystemSimulator().get_engine("sname").coupling_relation(h1, "trash", ch, "request")
            SystemSimulator().get_engine("sname").coupling_relation(ch, "check", g, ports[0])

            SystemSimulator().get_engine("sname").coupling_relation(g, ports[1], ch, "checked")
            SystemSimulator().get_engine("sname").coupling_relation(ch, "gov_report", gv, "recv_report")
    
            SystemSimulator().get_engine("sname").coupling_relation(None, "start", h1, "start")
            SystemSimulator().get_engine("sname").coupling_relation(None, "end", h1, "end")
            SystemSimulator().get_engine("sname").coupling_relation(h1, "trash", f, "receive_membertrash")
       

        SystemSimulator().get_engine("sname").register_entity(f)

        ports = g.register_family(j)
        SystemSimulator().get_engine("sname").coupling_relation(f, "takeout_trash", g, ports[0])
        j+=1

    # Connect Truck & Can
    ports = gt.register_garbage_can(i)
    SystemSimulator().get_engine("sname").coupling_relation(g, "res_garbage", gt, ports[0])
    SystemSimulator().get_engine("sname").coupling_relation(gt, ports[1], g, "req_empty")
    i+=1

SystemSimulator().get_engine("sname").insert_input_port("start")


SystemSimulator().get_engine("sname").coupling_relation(None, "start", c, "start")
SystemSimulator().get_engine("sname").coupling_relation(None, "end", c, "end")

#SystemSimulator().get_engine("sname").insert_external_event("report", None)
SystemSimulator().get_engine("sname").coupling_relation(None, "start", gt, "start")
SystemSimulator().get_engine("sname").coupling_relation(None, "end", gt, "end")

# Connect Truck & Can

SystemSimulator().get_engine("sname").insert_external_event("start", None)
SystemSimulator().get_engine("sname").simulate()


