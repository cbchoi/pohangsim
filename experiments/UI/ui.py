#GUI lib import
import os
import sys
import time
from functools import wraps

from PySide2.QtCore import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from data_component import Parameter
from garbage_truck import GarbageTruck

from pohangsim.check import Check
from pohangsim.clock import Clock
from pohangsim.core_component import FamilyType
from pohangsim.family import Family
from pohangsim.garbagecan import GarbageCan
from pohangsim.government import Government
from pohangsim.human import Human
from pohangsim.job import *
from util import scenario_editor  # scenario generator


# GUI lib import
# from config import *

def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.perf_counter()
        result = fn(*args, **kwargs)
        t2 = time.perf_counter()
        print("@timefn: {} took {} seconds".format(fn.__name__, t2 - t1))
        return result

    return measure_time




class ScenarioListManager(QDialog):
    SCENARIO_SIGNAL=Signal(list)
    def __init__(self, _parent =None):
        super(ScenarioListManager, self).__init__(_parent)
        self.obj= _parent
        self.dialog=None
        self.scenariolist=[]
        self.N=0

    def getBuildingNumber(self):
        text, ok = QInputDialog.getInt(self, 'Number of buildings', 'Enter the number of buildings')
        if ok:
            self.N = text
            self.newScenario()
    def newScenario(self): #빈 시나리오 생성
        if self.N <=0:
            msg = QMessageBox()
            msg.setWindowTitle("Try Again!")
            msg.setText("Wrong Value")
            msg.setDetailedText("Can generate scenario with positive integer number of buildings\nyour input value:{0}".format(self.N))
            msg.exec_()
        else:
            scenario=scenario_editor.new_scenario_GUI(self.N)
            scenario.memo="scenario"+str(scenario.id)
            self.listWidget.addItem(scenario.memo)
            self.scenariolist.append(scenario)

    def load_scenario(self):
        filename = QFileDialog.getOpenFileName()
        if filename[0]!='':
            scenario = scenario_editor.load_scenario_GUI(filename[0])
            self.listWidget.addItem(scenario.memo)
            #print(scenario,"here is laod scenario")
            self.scenariolist.append(scenario)
            self.SCENARIO_SIGNAL.emit(self.scenariolist)
    def new_scenario(self):
        ui_file = QFile("../../Dialog.ui")
        loader = QUiLoader()
        self.dialog = loader.load(ui_file)
        ui_file.close()
        self.dialog.setModal(True)
        self.dialog.show()
        self.dialog.buttonBox.accepted.connect(self.generate_scenario)
    
    def generate_scenario(self):
        a=self.dialog.StudentRatio.value()
        b=self.dialog.ConstructionWorkerRatio.value()
        c=self.dialog.HomemakerRatio.value()
        ratio_a=a/(a+b+c)
        ratio_b=b/(a+b+c)
        ratio_c=c/(a+b+c)
        N=int(self.dialog.N.toPlainText())
        if (ratio_a * N).is_integer() and (ratio_c * N).is_integer() and (ratio_c * N).is_integer():
            testcode(ratio_a,ratio_b,ratio_c,N,int(self.dialog.trials.toPlainText()),self.dialog.memo.toPlainText()) 
                                #testcode(ra,rb,rc,N,trial,memo)               
        else:
            print("wrong ratio and Number of residents")                            
            return False
        print("generate scenario")
        scenario=scenario_editor.ScenarioClass()
        scenario.load_from_file("./scenario/{0}_N{1}_seed{2}.txt".format(self.dialog.memo.toPlainText(),N,0))
        self.listWidget.addItem(scenario.memo)
        self.group.append(scenario)
        # 케이스가 생성된다 text파일로 scenario에 저장된다.
        self.SCENARIO_SIGNAL.emit(scenario)

    def save_scenario(self):
        if self.listWidget.count()<1:
            msg = QMessageBox()
            msg.setWindowTitle("Try Again!")
            msg.setText("Nothing to save")
            msg.setDetailedText(
                "Can only save loaded and generated scenario")
            msg.exec_()
        else:
            filename = QFileDialog.getSaveFileName()
            scenario_editor.save_scenario_GUI(self.scenariolist[self.listWidget.currentRow()],filename)

    
    def delete_scenario(self):
        listItems=self.listWidget.selectedItems()
        if not listItems: return        
        for item in listItems:
           self.listWidget.takeItem(self.listWidget.row(item))

    def __getattr__(self, attr):
        return getattr(self.obj, attr)



class MSWSsimulator(QWidget):
    def __init__(self, _parent =None):
        super(MSWSsimulator, self).__init__(_parent)
        self.obj= _parent
        self.obj.setWindowTitle("Pohangsim")
        self.simul_time=SimulTime(self.obj)
        self.controlbox=controlBox(self.obj)
        self.output=OutputManager(self.obj)
        self.ScenarioListControl=ScenarioListManager(self.obj)
        
        self.ScenarioListControl.SCENARIO_SIGNAL.connect(self.controlbox.prepare_data)
        #controlbox
        self.SimulateButton.clicked.connect(self.controlbox.prepare_data)
        
        #slider
        self.simulationtimeinput.valueChanged.connect(self.simul_time.synchro_slider)
        self.simulationtimeslider.valueChanged.connect(self.simul_time.synchro_spin)
        #scenario_control
        
        #self.new_button.clicked.connect(self.ScenarioListControl.new_scenario)
        self.new_button.clicked.connect(self.ScenarioListControl.getBuildingNumber)

        self.load_button.clicked.connect(self.ScenarioListControl.load_scenario)
        self.save_button.clicked.connect(self.ScenarioListControl.save_scenario)
        self.delete_button.clicked.connect(self.ScenarioListControl.delete_scenario)
        
        #timemode


        #controlbox
        self.controlbox.SIMULATE_SIGNAL.connect(self.controlbox.run_simulation)
        self.controlbox.SIMULATE_COMPLETE.connect(self.output.show_result)
    def __getattr__(self, attr):
        return getattr(self.obj, attr)
    def show(self):
        self.obj.show()
class timeMode(QObject):
    timemodeSignal=Signal(str)
    def __init__(self, _parent=None):
        super(timeMode,self).__init__(_parent)
        self.obj=_parent
        #self.

    def time_mode_select(self):
        if self.RealTime.isChecked():
            msg = "REAL_TIME"
        elif self.VirtualTime.isChecked():
            msg = "VIRTUAL_TIME"
        print("result is here")

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
    SIMULATE_SIGNAL=Signal(Parameter,scenario_editor.ScenarioClass)
    SIMULATE_COMPLETE=Signal()

    def __init__(self, _parent=None):
        super(controlBox, self).__init__(_parent)
        self.obj=_parent
        self.scenario=None
        self.parameter=Parameter()
        self.timer=QTimer()
        self.timer.timeout.connect(self.run_simulation)

    @Slot()
    def prepare_data(self,scenario_signal=False):
        if scenario_signal:
            self.scenario=scenario_signal
            #print(scenario_signal,"here is signal")
        
        self.parameter.TIME_DENSITY=self.TimeDensity.value()                             
        ###################################################
        self.parameter.AVG_TIME= self.AverageTime.value()
        self.parameter.AVG_TRASH = self.AverageTrash.value()
        self.parameter.GARBAGECAN_SIZE=    self.GarbageCanSize.value()
        self.parameter.TEMP_CAN_SIZE=     self.FamilyCanSize.value()
        self.parameter.GARBAGETRUCK_SIZE=   self.GarbageTruckSize.value()
        ###################################################
        self.parameter.TIME_STDDEV=   self.TimeStandardDeviation.value()
        self.parameter.TRASH_STDDEV= self.TrashStandardDeviation.value()      
        #self.parameter.TRUCK_INITIAL=    self.CollectionTime.value()
        self.parameter.TRUCK_INITIAL = 7
        self.parameter.TRUCK_CYCLE= 24
        #self.parameter.TRUCK_CYCLE = self.CollectionCycle.value()
        self.parameter.TRUCK_DELAY=    self.CollectionDelay.value()
        ###################################################
        self.parameter.simulation_time = 400
        #self.parameter.simulation_time= self.simulationtimeslider.value()
        if self.Verbosebox.isChecked():
            self.parameter.VERBOSE = True


        #parameter).SIMULATION_MODE=
        #parameter).RANDOM_SEED=   #새로 UI에 추가
        #parameter).VERBOSE=    #verbose가 체크됬을때 TRUE    
        self.parameter.update_config()
        if scenario_signal is False:
            self.SIMULATE_SIGNAL.emit(self.parameter,self.scenario)
    

    @Slot()
    @timefn
    def run_simulation(self,parameter,scenariolist):
        if scenariolist != None:
            if not os.path.exists("output"):
                os.makedirs("output")
            #print(parameter.__dict__.items())  #parameter 가제대로 왔는지 체크

            for scenario in scenariolist:
                filename = scenario.memo
                for kndx in range(5):
                    sys.stdout=sys.__stdout__
                    print(f"Processing {scenario.id}/{len(scenariolist)}:", scenario.memo)
                    sys.stdout = open("output/result_" + filename + "_" + str(kndx) + ".log", 'a')
                    if parameter.VERBOSE is True:
                        outputlocation = scenario.memo + str(parameter.TIME_STDDEV) + "trash" + str(
                            parameter.TRASH_STDDEV) + "_" + str(parameter.GARBAGECAN_SIZE) + "_" + str(kndx)
                        if not os.path.exists(outputlocation):
                            os.makedirs(outputlocation)
                    else:
                        outputlocation = None
                    se = SystemSimulator()

                    se.register_engine("sname", parameter.SIMULATION_MODE, parameter.TIME_DENSITY)

                    c = Clock(0, parameter.simulation_time, "clock", "sname")
                    se.get_engine("sname").register_entity(c)
                    gt = GarbageTruck(0, parameter.simulation_time, "garbage_truck", 'sname',
                                      parameter.GARBAGETRUCK_SIZE,
                                      [e for e in enumerate([parameter.TRUCK_DELAY for building in scenario])],
                                      outputlocation)  # 4.7*13*3
                    se.get_engine("sname").register_entity(gt)

                    gv = Government(0, parameter.simulation_time, "government", "sname")
                    se.get_engine("sname").register_entity(gv)
                    i = 0
                    j = 0

                    for building in scenario:
                        g = GarbageCan(0, parameter.simulation_time, "gc[{0}]".format(i), 'sname',
                                       parameter.GARBAGECAN_SIZE, outputlocation)
                        se.get_engine("sname").register_entity(g)

                        for flist in building:
                            ftype = FamilyType(parameter.TEMP_CAN_SIZE)
                            f = Family(0, parameter.simulation_time, "family", 'sname', ftype)
                            for htype in flist:
                                # hid = get_human_id()
                                name = htype.get_name()
                                cname = "check[{0}]".format(htype.get_name())
                                h1 = Human(0, parameter.simulation_time, cname, "sname", htype)
                                ch = Check(0, parameter.simulation_time, name, "sname", htype)

                                se.get_engine("sname").register_entity(h1)
                                se.get_engine("sname").register_entity(ch)
                                # f1.register_member(htype)
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
                            j += 1

                        # Connect Truck & Can

                        ports = gt.register_garbage_can(i)
                        se.get_engine("sname").coupling_relation(g, "res_garbage", gt, ports[0])
                        se.get_engine("sname").coupling_relation(gt, ports[1], g, "req_empty")
                        i += 1

                    se.get_engine("sname").insert_input_port("start")

                    se.get_engine("sname").coupling_relation(None, "start", c, "start")
                    se.get_engine("sname").coupling_relation(None, "end", c, "end")

                    # se.get_engine("sname").insert_external_event("report", None)
                    se.get_engine("sname").coupling_relation(None, "start", gt, "start")
                    se.get_engine("sname").coupling_relation(None, "end", gt, "end")

                    # Connect Truck & Can

                    se.get_engine("sname").insert_external_event("start", None)
                    se.get_engine("sname").simulate()


        #self.SIMULATE_COMPLETE.emit() #시뮬레이션 완료 신호 # 시뮬레이터가 종료되고 나서 시그널을 보내야함
    
    def __getattr__(self, attr):
        return getattr(self.obj, attr)
