import contexts

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

c = Clock(0, 50, "clock", "sname")
SystemSimulator().get_engine("sname").register_entity(c)

g = GarbageCan(0, 50, "gc", 'sname', 10)

SystemSimulator().get_engine("sname").register_entity(g)

h_id = 0

def get_human_id():
    global h_id
    h_id += 1
    return h_id
    
hlist1 = [Self_employment(get_human_id()),Self_employment(get_human_id())]
hlist2=[Self_employment(get_human_id()),Self_employment(get_human_id()),Student(get_human_id())]
hlist3=[Student(get_human_id()),Student(get_human_id())]
hlist4=[Student(get_human_id())]
hlist5=[Housewife(get_human_id()),Blue_collar(get_human_id()),Inoccupation(get_human_id()),Student(get_human_id())]
hlist6=[White_collar(get_human_id()),White_collar(get_human_id()),Inoccupation(get_human_id())]
hlist7=[Blue_collar(get_human_id()),Blue_collar(get_human_id()),Blue_collar(get_human_id())]
hlist8=[Blue_collar(get_human_id()),Blue_collar(get_human_id()),Blue_collar(get_human_id())]
hlist9=[AFF(get_human_id()),Inoccupation(get_human_id()),Housewife(get_human_id())]
hlist10=[White_collar(get_human_id()),White_collar(get_human_id()),Housewife(get_human_id())]


test1=[hlist1,hlist2,hlist3,hlist4,hlist5,hlist6,hlist7,hlist8,hlist9,hlist10]

gv = Government(0,50,"government","sname")

gv = Government(0,50,"government","sname")

SystemSimulator().get_engine("sname").register_entity(gv)

i=0
for family in test1:
    print ("###")
    i+=1
    globals()['ftype{}'.format(i)]= FamilyType(5*len(family))

    globals()['f{}'.format(i)] = Family(0, 50,"family",'sname', globals()['ftype{}'.format(i)])

    for htype in family:
        hid = htype.get_id()
        name = "aff[{0}]".format(hid)
        cname = "check[{0}]".format(hid)

        ch = Check(0, 50, cname, "sname", htype.get_satisfaction_func)
        h1 = Human(0, 50, name, "sname", htype)

        SystemSimulator().get_engine("sname").register_entity(h1)
        SystemSimulator().get_engine("sname").register_entity(ch)
    
    #f1.register_member(htype)
        globals()['ftype{}'.format(i)].register_member(htype)
    
        ports = ch.register_human(hid)
        SystemSimulator().get_engine("sname").coupling_relation(h1, "trash", ch, ports[0])

        SystemSimulator().get_engine("sname").coupling_relation(ch, "check", g,"check_garbage")

        SystemSimulator().get_engine("sname").coupling_relation(g, "res_check", ch, "checked")
        SystemSimulator().get_engine("sname").coupling_relation(ch, "gov_report", gv, "recv_report")
    
        SystemSimulator().get_engine("sname").coupling_relation(None, "start", h1, "start")
        SystemSimulator().get_engine("sname").coupling_relation(None, "end", h1, "end")
        SystemSimulator().get_engine("sname").coupling_relation(h1, "trash", globals()['f{}'.format(i)], "receive_membertrash")
    
        SystemSimulator().get_engine("sname").register_entity(globals()['f{}'.format(i)])
    SystemSimulator().get_engine("sname").coupling_relation(globals()['f{}'.format(i)], "takeout_trash", g, "recv_garbage")

SystemSimulator().get_engine("sname").insert_input_port("start")


SystemSimulator().get_engine("sname").coupling_relation(None, "start", c, "start")
SystemSimulator().get_engine("sname").coupling_relation(None, "end", c, "end")

#SystemSimulator().get_engine("sname").insert_external_event("report", None)


SystemSimulator().get_engine("sname").insert_external_event("start", None)
SystemSimulator().get_engine("sname").simulate()
