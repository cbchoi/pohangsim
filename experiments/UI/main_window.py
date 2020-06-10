#GUI lib import
import contexts
import sys,os
import math

from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_simulator import SystemSimulator
from evsim.definition import *
import functools

from PySide2.QtCore import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *


from data_component import Parameter
#from garbage_truckpalindrome import GarbageTruck
from garbage_truckfixed import GarbageTruck
#from garbage_truckrandom import GarbageTruck

from pohangsim.check import Check
from pohangsim.clock import Clock
from pohangsim.core_component import HumanType,FamilyType
from pohangsim.family import Family
from pohangsim.garbagecan import GarbageCan
from pohangsim.government import Government
from pohangsim.human import Human
from pohangsim.job import *

from pohangsim.signal_model import SignalLoop
from scenario_editor import FamilyClass,BuildingClass,ScenarioClass,new_scenario_GUI,load_scenario_GUI,save_scenario_GUI
from building_dialog import BuildingTypeManager
#matplot
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
#from matplot import resultWidget



# GUI lib import
# from config import *
class ScenarioListManager(QDialog):
    SCENARIO_SIGNAL=Signal(list)
    def __init__(self, _parent =None):
        super(ScenarioListManager, self).__init__(_parent)
        self.obj= _parent
        self.dialog=BuildingTypeManager
        self.scenariolist=[]
        self.selected_scenario=ScenarioClass
        self.N=0
        self.familytypelist=[]

    @Slot()
    def get_familytype(self,list1,list2):
        self.familytypelist=list1
        self.selected_scenario=list2
        self.scenariolist[self.listWidget.currentRow()]=self.selected_scenario

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
            scenario= new_scenario_GUI(self.N)
            scenario.memo="scenario"+str(scenario.id)
            self.listWidget.addItem(scenario.memo)
            self.scenariolist.append(scenario)

    def load_scenario(self):
        filename = QFileDialog.getOpenFileName()
        if filename[0]!='':
            scenario,familytype = load_scenario_GUI(filename[0])
            filename=filename[0].split('/')
            self.listWidget.addItem(filename[-1])
            #print(scenario,"here is laod scenario")
            self.scenariolist.append(scenario)
            self.familytypelist=familytype
    def edit_scenario(self):
        if self.listWidget.currentRow()>=0:

            self.selected_scenario=self.scenariolist[self.listWidget.currentRow()]
            ui_file = QFile("../../BuildingDialog.ui")
            loader = QUiLoader()
            self.dialog= loader.load(ui_file)
            ui_file.close()
            self.dialog.setModal(True)
            self.dialog=BuildingTypeManager(self.familytypelist,self.selected_scenario,self.dialog)
            self.dialog.show()
        #빌딩을 로딩

    def send_scenario(self):
        if self.listWidget.currentRow() >=0:
            self.SCENARIO_SIGNAL.emit(self.scenariolist[self.listWidget.currentRow()])
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Try Again!")
            msg.setText("Select scenario to simulate")
            msg.setDetailedText(
                "No scenario is selected!")
            msg.exec_()
    
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
            save_scenario_GUI(self.scenariolist[self.listWidget.currentRow()],self.familytypelist, filename)

    def delete_scenario(self):
        listItems=self.listWidget.selectedItems()
        if not listItems: return
        for item in listItems:
            self.listWidget.takeItem(self.listWidget.row(item))
            del self.scenariolist[self.listWidget.row(item)]

    def __getattr__(self, attr):
        return getattr(self.obj, attr)


class DataGroupHandler(QObject):
    DATA_SIG = Signal(list)

    def __init__(self, _parent=None):
        super(DataGroupHandler, self).__init__(_parent)
        self.obj = _parent
        #self.editX.setText('0')
        #self.editY.setText('0')
        self._data_points = []
        pass

    def load(self):
        self._data_points.append((int(self.editX.text()), int(self.editY.text())))
        self.listWidget.addItem("({0}, {1})".format(self._data_points[-1][0], self._data_points[-1][1]))
        self.DATA_SIG.emit(self._data_points)

    def clearBtn(self):
        self._data_points = []

    def __getattr__(self, attr):
        return getattr(self.obj, attr)

class resultWidget(QObject):
    def __init__(self, _parent=None):
        super(resultWidget, self).__init__(_parent)
        self.obj = _parent

        self.dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.resultLayout.addWidget(self.dynamic_canvas)

        self._dynamic_ax = self.dynamic_canvas.figure.subplots()
        self._data_controller = DataGroupHandler(_parent)

        self._data_controller.DATA_SIG.connect(self._update_canvas)

    def __getattr__(self, attr):
        return getattr(self.obj, attr)

    def show(self):
        self.obj.show()

    @Slot(list)
    def _update_canvas(self, points):
        self._dynamic_ax.clear()
        unzipped = list(zip(*points))
        print("update", *unzipped)

        self.x_data, self.y_data = unzipped[0], unzipped[1]

        if self.radioPlot.isChecked():
            self._dynamic_ax.plot(unzipped[0], unzipped[1])
        elif self.radioPie.isChecked():
            self._dynamic_ax.pie(upzipped[1])
        else:
            self._dynamic_ax.bar(unzipped[0], unzipped[1])

        self.dynamic_canvas.figure.canvas.draw()
        self.obj.repaint()

    @Slot()
    def _redraw_graph(self):
        self._dynamic_ax.clear()
        if self.radioPlot.isChecked():
            self._dynamic_ax.plot(self.x_data, self.y_data)
        elif self.radioPie.isChecked():
            self._dynamic_ax.pie(self.y_data)
        else:
            self._dynamic_ax.bar(self.x_data, self.y_data)

        self.dynamic_canvas.figure.canvas.draw()
        self.obj.repaint()

        pass
class MSWSsimulator(QWidget):
    def __init__(self, _parent =None):
        super(MSWSsimulator, self).__init__(_parent)
        self.obj= _parent
        self.dialog=None
        self.obj.setWindowTitle("Pohangsim")
        self.simul_time=SimulTime(self.obj)
        self.controlbox=controlBox(self.obj)
        self.output=OutputManager(self.obj)
        self.ScenarioListControl=ScenarioListManager(self.obj)
        self.MatplotResult=resultWidget(self.obj)
        self.ScenarioListControl.dialog.signal.LISTSIG.connect(self.ScenarioListControl.get_familytype)
        #기본을 벌츄얼 타임으로
        self.VirtualTime.setChecked(True)
        #controlbox
        #Simulate 버튼 클릭시
        self.controlbox.SimulateButton.clicked.connect(self.ScenarioListControl.send_scenario) #scenario list 전달
        self.ScenarioListControl.SCENARIO_SIGNAL.connect(self.controlbox.prepare_data) #parameter 읽기 -> timerstart
        #simulation이 끝나면 결과
        self.controlbox.READY_SIG.connect(self.controlbox.timer_start)
        #self.controlbox.READY_SIG.connect(self.controlbox.timer_start) # ready - > loopback -> result
        #self.controlbox.loopback.signal.LOOPBACK_SIG.connect(self.controlbox.run_simulate)
        self.controlbox.RESULT_SIGNAL.connect(self.output.show_result)
        


        self.StopButton.clicked.connect(self.controlbox.stop_button)
        
        #slider
        self.simulationtimeinput.valueChanged.connect(self.simul_time.synchro_slider)
        self.simulationtimeslider.valueChanged.connect(self.simul_time.synchro_spin)
        #scenario_control
        
        #self.new_button.clicked.connect(self.ScenarioListControl.new_scenario)
        self.new_button.clicked.connect(self.ScenarioListControl.getBuildingNumber)
        self.load_button.clicked.connect(self.ScenarioListControl.load_scenario)
        self.edit_button.clicked.connect(self.ScenarioListControl.edit_scenario)
        self.save_button.clicked.connect(self.ScenarioListControl.save_scenario)
        self.delete_button.clicked.connect(self.ScenarioListControl.delete_scenario)
        

    def __getattr__(self, attr):
        return getattr(self.obj, attr)
    def show(self):
        self.obj.show()

class OutputManager(QObject):
    def __init__(self, _parent=None):
        super(OutputManager,self).__init__(_parent)
        self.obj=_parent
        self.dialog=None

    @Slot()
    def show_result(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText("Simulation is finished")
        msg.exec_()


        #self.resultWidget
        pass
        """
        QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
        ui_file = QFile("../../Output.ui")
        self.dialog= QUiLoader.load(ui_file)
        ui_file.close()
        self.dialog.setModal(False)
        #self.dialog=MatplotlibExample(self.dialog)
        self.dialog.show()
        """

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
    SIMULATE_SIGNAL=Signal(Parameter, list)
    READY_SIG=Signal()
    RESULT_SIGNAL=Signal()
    def __init__(self, _parent=None):
        super(controlBox, self).__init__(_parent)
        self.obj=_parent
        self.scenario=None
        self.parameter=Parameter()
        self.worker=QTimer()

        self.loopback=SignalLoop
        self.timer=0
    @Slot()
    def timer_start(self):
        self.progressBar.setMaximum(self.parameter.simulation_time)
        self.timer=0
        self.worker.timeout.connect(self.run_simulate)
        self.worker.start(1)

    def stop_button(self):
        if self.timer!=0:
            SystemSimulator().get_engine("sname").simulation_stop()
            self.worker.stop()
            self.timer = 0
            msg = QMessageBox()
            msg.setWindowTitle("Stopped!")
            msg.setText("Simulation Stopped")
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Already Stopped!")
            msg.setText("Nothing to stop")
            msg.exec_()
    @Slot()
    def result_show(self):
        print("signal model is working")
        pass
    
    @Slot()
    def progress_show(self):
        print("loopback signal")

    @Slot()
    def prepare_data(self,scenario_signal=False):
        if scenario_signal:
            self.scenario=scenario_signal
        if self.RealTime.isChecked():
            self.parameter.SIMULATION_MODE = "REAL_TIME"
        elif self.VirtualTime.isChecked():
            self.parameter.SIMULATION_MODE = "VIRTUAL_TIME"
        self.parameter.TIME_DENSITY = self.TimeDensity.value()
        self.parameter.AVG_TIME = self.AverageTime.value()
        self.parameter.AVG_TRASH = self.AverageTrash.value()
        self.parameter.GARBAGECAN_SIZE = self.GarbageCanSize.value()
        self.parameter.TEMP_CAN_SIZE = self.FamilyCanSize.value()
        self.parameter.GARBAGETRUCK_SIZE = self.GarbageTruckSize.value()
        self.parameter.TIME_STDDEV=   self.TimeStandardDeviation.value()
        self.parameter.TRASH_STDDEV= self.TrashStandardDeviation.value()
        self.parameter.TRUCK_CYCLE = self.CollectionCycle.value()
        self.parameter.TRUCK_DELAY=    self.CollectionDelay.value()
        self.parameter.TRUCK_INITIAL=    self.CollectionTime.value()
        self.parameter.simulation_time = self.simulationtimeslider.value()
        ###################################################
        

        if self.Verbosebox.isChecked():
            self.parameter.VERBOSE = True
        else:
            self.parameter.VERBOSE = False
        #self.parameter.VERBOSE = True
        self.parameter.update_config()
        self.loopback = SignalLoop(0, self.parameter.simulation_time, "loopback", "sname")
        if self.scenario==None:
            print("error message here")
        else:
            self.simulation_initialize()

    def simulation_initialize(self):
        if not os.path.exists("output"):
            os.makedirs("output")
        if self.parameter.VERBOSE is True:
            outputlocation = self.scenario.memo +"_"+ str(self.parameter.TIME_STDDEV) + "trash" + str(
                self.parameter.TRASH_STDDEV) + "_" + str(self.parameter.GARBAGECAN_SIZE)
            if not os.path.exists(outputlocation):
                os.makedirs(outputlocation)
        else:
            outputlocation = None
        se = SystemSimulator()
        se.register_engine("sname", self.parameter.SIMULATION_MODE, self.parameter.TIME_DENSITY)
        se.get_engine("sname").register_entity(self.loopback)
        c = Clock(0, self.parameter.simulation_time, "clock", "sname")
        se.get_engine("sname").register_entity(c)
        gt = GarbageTruck(0, self.parameter.simulation_time, "garbage_truck", 'sname',
                          self.parameter.GARBAGETRUCK_SIZE,
                          [e for e in enumerate([self.parameter.TRUCK_DELAY for building in self.scenario])],
                          outputlocation)  # 4.7*13*3
        se.get_engine("sname").register_entity(gt)
        gv = Government(0, self.parameter.simulation_time, "government", "sname")
        se.get_engine("sname").register_entity(gv)
        i = 0
        j = 0
        id=0
        for building in self.scenario:
            g = GarbageCan(0, self.parameter.simulation_time, "gc[{0}]".format(i), 'sname',
                           self.parameter.GARBAGECAN_SIZE, outputlocation)
            se.get_engine("sname").register_entity(g)
            for flist in building:
                ftype = FamilyType(self.parameter.TEMP_CAN_SIZE)
                f = Family(0, self.parameter.simulation_time, "family", 'sname', ftype)
                for htype in flist:
                    id+=1
                    name = htype.get_name()
                    name= name.split('<')[0]+"("+ str(id)+")"
                    cname = "check[{0}]".format(name)
                    h1 = Human(0, self.parameter.simulation_time, cname, "sname", htype)
                    ch = Check(0, self.parameter.simulation_time, name, "sname", htype)
                    se.get_engine("sname").register_entity(h1)
                    se.get_engine("sname").register_entity(ch)
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
        se.get_engine("sname").coupling_relation(None, "start", gt, "start")
        se.get_engine("sname").coupling_relation(None, "end", gt, "end")
        # Connect Truck & Can
        se.get_engine("sname").coupling_relation(None,"start",self.loopback,"start")
        # end of simulation signal
        se.get_engine("sname").insert_external_event("start", None)
        self.READY_SIG.emit()

    def run_simulate(self):
        self.timer+=1
        SystemSimulator().get_engine("sname").simulate(self.timer)
        sim_t=SystemSimulator().get_engine("sname").get_global_time()
        self.progressBar.setValue(sim_t)
        if sim_t/self.parameter.simulation_time>=1:
            self.worker.stop()
            SystemSimulator().get_engine("sname").simulation_stop()
            self.timer=0
            self.progressBar.setValue(self.parameter.simulation_time)
            self.RESULT_SIGNAL.emit()

    def __getattr__(self, attr):
        return getattr(self.obj, attr)
