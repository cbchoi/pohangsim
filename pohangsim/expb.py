import contexts
import sys,os

from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

from config import *

from clock import Clock
from core_component import HumanType
from core_component import FamilyType

from job import *

from human import Human
from check import Check
from government import Government
from garbagecan import GarbageCan
from garbage_truck import GarbageTruck
from family import Family

blist=[]
hlist=[]
fam=[]
outputlocation=str(sys.argv[1])+str(TIME_STDDEV)
if not os.path.exists(outputlocation):
    os.makedirs(outputlocation)

file = open('update/b1.txt','r')
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

se.register_engine("sname", SIMULATION_MODE, TIME_DENSITY)

c = Clock(0, simulation_time, "clock", "sname")
se.get_engine("sname").register_entity(c)
gt = GarbageTruck(0, simulation_time, "garbage_truck", 'sname', GARBAGETRUCK_SIZE, [e for e in enumerate([TRUCK_DELAY for building in blist])],outputlocation)#4.7*13*3
se.get_engine("sname").register_entity(gt)

gv = Government(0, simulation_time,"government","sname")
se.get_engine("sname").register_entity(gv)

#Building Register

i=0
j=0
for building in blist:


    g = GarbageCan(0, simulation_time, "gc[{0}]".format(i), 'sname', GARBAGECAN_SIZE,outputlocation)
    se.get_engine("sname").register_entity(g)
    
    for flist in building:
        ftype = FamilyType(TEMP_CAN_SIZE)
        f = Family(0, simulation_time,"family",'sname', ftype)
        for htype in flist:
            #hid = get_human_id()
            name = htype.get_name()
            cname = "check[{0}]".format(htype.get_name())               
            h1 = Human(0, simulation_time, cname, "sname", htype)
            ch = Check(0, simulation_time, name, "sname", htype)

            se.get_engine("sname").register_entity(h1)
            se.get_engine("sname").register_entity(ch)
            #f1.register_member(htype)
            ftype.register_member(htype)
            
            # Connect Check & Can
            ports = g.register_human(htype.get_id())
            se.get_engine("sname").coupling_relation(h1, "trash", ch, "request")
            se.get_engine("sname").coupling_relation(ch, "check", g, ports[0])

            se.get_engine("sname").coupling_relation(g, ports[1], ch, "checked")
            se.get_engine("sname").coupling_relation(ch, "gov_report", gv, "recv_report")
    
            se.get_engine("sname").coupling_relation(None, "start", h1, "start")
            se.get_engine("sname").coupling_relation(None, "end", h1, "end")
            se.get_engine("sname").coupling_relation(h1, "trash", f, "receive_membertrash")
       

        se.get_engine("sname").register_entity(f)

        ports = g.register_family(j)
        se.get_engine("sname").coupling_relation(f, "takeout_trash", g, ports[0])
        j+=1

    # Connect Truck & Can
    ports = gt.register_garbage_can(i)
    se.get_engine("sname").coupling_relation(g, "res_garbage", gt, ports[0])
    se.get_engine("sname").coupling_relation(gt, ports[1], g, "req_empty")
    i+=1

se.get_engine("sname").insert_input_port("start")


se.get_engine("sname").coupling_relation(None, "start", c, "start")
se.get_engine("sname").coupling_relation(None, "end", c, "end")

#se.get_engine("sname").insert_external_event("report", None)
se.get_engine("sname").coupling_relation(None, "start", gt, "start")
se.get_engine("sname").coupling_relation(None, "end", gt, "end")

# Connect Truck & Can

se.get_engine("sname").insert_external_event("start", None)
se.get_engine("sname").simulate()


