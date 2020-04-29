#GUI lib import
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import *
from PySide2.QtGui import *
#GUI lib import

import contexts
import sys,os

from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

from config import * # 이것  대신에 GUI에서 받은 데이터가 들어가야함

from pohangsim.clock import Clock
from pohangsim.core_component import HumanType
from pohangsim.core_component import FamilyType

from pohangsim.job import *

from pohangsim.human import Human
from pohangsim.check import Check
from pohangsim.government import Government
from pohangsim.garbagecan import GarbageCan
from garbage_truck import GarbageTruck
from pohangsim.family import Family 
from util.case_generator import * #scenario generator

class Parameter:
    def __init__(self):
        self.TIME_DENSITY=0
        self.AVG_TIME=0
        self.AVG_TRASH=0
        self.GARBAGECAN_SIZE=0
        self.TEMP_CAN_SIZE=0
        self.GARBAGETRUCK_SIZE=0
        self.TIME_STDDEV=0
        self.TRASH_STDDEV=0
        self.TRUCK_INITIAL=0
        self.TRUCK_CYCLE=0
        self.TRUCK_DELAY=0
        self.simulation_time=0
        self.text=""
        ################################ 
        pass
        self.SIMULATION_MODE='VIRTUAL_TIME'
        self.RANDOM_SEED=0
        self.VERBOSE=False
    
    def update_config(self):
        self.text=  "TIME_DENSITY="+str(self.TIME_DENSITY)+"\nAVG_TIME="+str(self.AVG_TIME)+"\nAVG_TRASH="+str(self.AVG_TRASH)+"\nGARBAGECAN_SIZE="+str(self.GARBAGECAN_SIZE)+"\nTEMP_CAN_SIZE="+str(self.TEMP_CAN_SIZE)+"\nGARBAGETRUCK_SIZE="+str(self.GARBAGETRUCK_SIZE)+"\nTIME_STDDEV="+str(self.TIME_STDDEV)+"\nTRASH_STDDEV="+str(self.TRASH_STDDEV)+"\nTRUCK_INITIAL="+str(self.TRUCK_INITIAL)+"\nTRUCK_CYCLE="+str(self.TRUCK_CYCLE)+"\nTRUCK_DELAY="+str(self.TRUCK_DELAY)+"\nsimulation_time="+str(self.simulation_time)
        file=open("config.py","w")
        file.write(self.text)

class MSWSsimulator(QWidget):
    def __init__(self, _parent =None):
        super(MSWSsimulator, self).__init__(_parent)
        self.obj= _parent
        self.simul_time=SimulTime(self.obj)
        self.controlbox=controlBox(self.obj)
        self.output=OutputManager(self.obj)
        #controlbox
        self.SimulateButton.clicked.connect(self.controlbox.simulate)
        #slider
        self.simulationtimeinput.valueChanged.connect(self.simul_time.synchro_slider)
        self.simulationtimeslider.valueChanged.connect(self.simul_time.synchro_spin)
        
        self.controlbox.SIMULATE_SIGNAL.connect(self.controlbox.run_simulation)
        self.controlbox.SIMULATE_COMPLETE.connect(self.output.show_result)
    def __getattr__(self, attr):
        return getattr(self.obj, attr)
    def show(self):
        self.obj.show()

class OutputManager(QObject):
    def __init__(self, _parent=None):
        super(OutputManager,self).__init__(_parent)
        self.obj=_parent

    @Slot()
    def show_result(self):
        print("result is here")
        pass

class SimulTime(QObject):
    def __init__(self, _parent=None):
        super(SimulTime,self).__init__(_parent)
        self.obj=_parent
    
    def synchro_spin(self):
        self.simulationtimeinput.setValue(self.simulationtimeslider.value())
        
    def synchro_slider(self):
        self.simulationtimeslider.setValue(self.simulationtimeinput.value())

    def __getattr__(self, attr):
        return getattr(self.obj, attr)

class controlBox(QObject):
    #signal part
    SIMULATE_SIGNAL=Signal(Parameter)
    SIMULATE_COMPLETE=Signal()

    def __init__(self, _parent=None):
        super(controlBox, self).__init__(_parent)
        self.obj=_parent
    @Slot()
    def simulate(self):
        parameter=Parameter()
        parameter.TIME_DENSITY=self.TimeDensity.value()                             
        ###################################################
        parameter.AVG_TIME= self.AverageTime.value()
        parameter.AVG_TRASH = self.AverageTrash.value()
        parameter.GARBAGECAN_SIZE=    self.GarbageCanSize.value()
        parameter.TEMP_CAN_SIZE=     self.FamilyCanSize.value()
        parameter.GARBAGETRUCK_SIZE=   self.GarbageTruckSize.value()
        ###################################################
        parameter.TIME_STDDEV=   self.TimeStandardDeviation.value()
        parameter.TRASH_STDDEV= self.TrashStandardDeviation.value()      
        parameter.TRUCK_INITIAL=    self.CollectionTime.value()
        parameter.TRUCK_CYCLE=    self.CollectionCycle.value()
        parameter.TRUCK_DELAY=    self.CollectionDelay.value()
        ###################################################

        parameter.simulation_time= self.simulationtimeslider.value()
        #parameter).SIMULATION_MODE=    
        #parameter).RANDOM_SEED=   #새로 UI에 추가
        #parameter).VERBOSE=    #verbose가 체크됬을때 TRUE    
        parameter.update_config()
        self.SIMULATE_SIGNAL.emit(parameter)
    
    @Slot()
    def run_simulation(self,parameter):
        print(parameter.__dict__.items())
        pass
"""
        for kndx in range(30):
            hlist=[]
            blist=[]
            fam=[]

            if parameter.VERBOSE is True:
                outputlocation=str(sys.argv[1])+str(parameter.TIME_STDDEV)+"trash"+str(parameter.TRASH_STDDEV)+"_"+str(parameter.GARBAGECAN_SIZE)+"_"+str(kndx)
                if not os.path.exists(outputlocation):
                    os.makedirs(outputlocation)
            else:
                outputlocation = None

            #scenario input방식을 바꾸어야함
            file = open("./scenario/"+sys.argv[1]+".txt",'r')
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

            se.register_engine("sname", parameter.SIMULATION_MODE, parameter.TIME_DENSITY)

            c = Clock(0, parameter.simulation_time, "clock", "sname")
            se.get_engine("sname").register_entity(c)
            gt = GarbageTruck(0, parameter.simulation_time, "garbage_truck", 'sname', parameter.GARBAGETRUCK_SIZE, [e for e in enumerate([parameter.TRUCK_DELAY for building in blist])],outputlocation)#4.7*13*3
            se.get_engine("sname").register_entity(gt)

            gv = Government(0, parameter.simulation_time,"government","sname")
            se.get_engine("sname").register_entity(gv)

            #Building Register

            i=0
            j=0
            for building in blist:
                g = GarbageCan(0, parameter.simulation_time, "gc[{0}]".format(i), 'sname', parameter.GARBAGECAN_SIZE, outputlocation)
                se.get_engine("sname").register_entity(g)
                
                for flist in building:
                    ftype = FamilyType(parameter.TEMP_CAN_SIZE)
                    f = Family(0, parameter.simulation_time,"family",'sname', ftype)
                    for htype in flist:
                        #hid = get_human_id()
                        name = htype.get_name()
                        cname = "check[{0}]".format(htype.get_name())               
                        h1 = Human(0, parameter.simulation_time, cname, "sname", htype)
                        ch = Check(0, parameter.simulation_time, name, "sname", htype)

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
"""

        self.SIMULATE_COMPLETE.emit() #시뮬레이션 완료 신호
    
    def __getattr__(self, attr):
        return getattr(self.obj, attr)




class ScenarioManager(QDialog):
     def __init__(self, _parent =None):
        super(ScenarioManager, self).__init__(_parent)

    def generate_scenario(ratio_a,ratio_b,ratio_c,trial,s):
        memo=str(s)
        testcode(ratio_a,ratio_b,ratio_c,trial,memo) 
        # 케이스가 생성된다 text파일로 scenario에 저장된다.

    def load_scenario():
        pass
    def save_scenario():
        pass


#UI Loading Code

app = QApplication(sys.argv)

ui_file = QFile("PohangSim.ui")
loader = QUiLoader()
window = loader.load(ui_file)
ui_file.close()

pohangMSWS=MSWSsimulator(window)
pohangMSWS.show()

    
sys.exit(app.exec_())


