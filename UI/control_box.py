import os
import sys
from datetime import datetime
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from UI.data_component import Parameter

from UI.garbage_truckfixed import GarbageTruck as GarbageTruckf
from UI.garbage_truckpalindrome import GarbageTruck as GarbageTruckp
from UI.garbage_truckrandom import GarbageTruck as GarbageTruckr
#
from pohangsim.check import Check
from pohangsim.clock import Clock
from pohangsim.core_component import FamilyType
from pohangsim.family import Family
from pohangsim.garbagecan import GarbageCan
from pohangsim.government import Government
from pohangsim.human import Human
from pohangsim.job import *
from pohangsim.signal_model import SignalLoop

class controlBox(QObject):
    # signal part
    SIMULATE_SIGNAL = Signal(Parameter, list)
    READY_SIG = Signal()
    RESULT_SIGNAL = Signal(int,str)

    def __init__(self, _parent=None):
        super(controlBox, self).__init__(_parent)
        self.obj = _parent
        self.scenario = None
        self.parameter = Parameter()
        self.worker = QTimer()
        self.outputlocation=""
        self.loopback = SignalLoop
        self.timer = 0
        self.now=str
        self.progressBar.setVisible(False)

    @Slot()
    def timer_start(self):
        self.progressBar.setVisible(True)
        self.progressBar.setMaximum(self.parameter.simulation_time)
        self.timer = 0
        self.worker.timeout.connect(self.run_simulate)
        self.worker.start(1)

    def stop_button(self):
        if self.timer != 0:
            SystemSimulator().get_engine("sname").simulation_stop()
            self.worker.stop()
            self.timer = 0
            self.progressBar.setValue(0)
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
    def prepare_data(self, scenario_signal=False):
        if scenario_signal:
            self.scenario = scenario_signal
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
        self.parameter.TIME_STDDEV = self.TimeStandardDeviation.value()
        self.parameter.TRASH_STDDEV = self.TrashStandardDeviation.value()
        self.parameter.TRUCK_CYCLE = self.CollectionCycle.value()
        self.parameter.TRUCK_DELAY = self.CollectionDelay.value()
        self.parameter.TRUCK_INITIAL = self.CollectionTime.value()
        self.parameter.simulation_time = self.simulationtimeslider.value()
        self.parameter.RANDOM_SEED=self.Rseed.value()
        ###################################################

        if self.Verbosebox.isChecked():
            self.parameter.VERBOSE = True
        else:
            self.parameter.VERBOSE = False
        # self.parameter.VERBOSE = True
        self.parameter.update_config()
        self.loopback = SignalLoop(0, self.parameter.simulation_time, "loopback", "sname")
        if self.scenario == None:
            print("error message here")
        else:

            self.simulation_initialize()

    def simulation_initialize(self):
        self.now =str(datetime.now()).split()[1].replace(":","_")
        if not os.path.exists("output"):
            os.makedirs("output")

        if self.parameter.VERBOSE is True:
            self.outputlocation ="verbose/"+ self.scenario.memo + "_" + str(self.parameter.TIME_STDDEV) + "trash" + str(
                self.parameter.TRASH_STDDEV) + "_" + str(self.parameter.GARBAGECAN_SIZE) +self.now
            if not os.path.exists(self.outputlocation):
                os.makedirs(self.outputlocation)
        else:
            self.outputlocation = None
        sys.stdout=open("output/"+self.scenario.memo + "_" + str(self.parameter.TIME_STDDEV) + "trash" + str(self.parameter.TRASH_STDDEV) + "_" + str(self.parameter.GARBAGECAN_SIZE)+self.now+".log",'a')
        se = SystemSimulator()
        se.register_engine("sname", self.parameter.SIMULATION_MODE, self.parameter.TIME_DENSITY)
        se.get_engine("sname").register_entity(self.loopback)
        c = Clock(0, self.parameter.simulation_time, "clock", "sname")
        se.get_engine("sname").register_entity(c)
        if self.radioButton.isChecked():
            gt = GarbageTruckf(0, self.parameter.simulation_time, "garbage_truck", 'sname',
                              self.parameter.GARBAGETRUCK_SIZE,
                              [e for e in enumerate([self.parameter.TRUCK_DELAY for building in self.scenario])],
                              self.outputlocation)  # 4.7*13*3
        elif self.radioButton_2.isChecked():
            gt = GarbageTruckp(0, self.parameter.simulation_time, "garbage_truck", 'sname',
                               self.parameter.GARBAGETRUCK_SIZE,
                               [e for e in enumerate([self.parameter.TRUCK_DELAY for building in self.scenario])],
                               self.outputlocation)  # 4.7*13*3
        elif self.radioButton_3.isChecked():
            gt = GarbageTruckr(0, self.parameter.simulation_time, "garbage_truck", 'sname',
                               self.parameter.GARBAGETRUCK_SIZE,
                               [e for e in enumerate([self.parameter.TRUCK_DELAY for building in self.scenario])],
                               self.outputlocation)  # 4.7*13*3

        se.get_engine("sname").register_entity(gt)
        gv = Government(0, self.parameter.simulation_time, "government", "sname")
        se.get_engine("sname").register_entity(gv)
        i = 0
        j = 0
        for building in self.scenario:
            g = GarbageCan(0, self.parameter.simulation_time, "gc[{0}]".format(i), 'sname',
                           self.parameter.GARBAGECAN_SIZE, self.outputlocation)
            se.get_engine("sname").register_entity(g)
            for flist in building:
                ftype = FamilyType(self.parameter.TEMP_CAN_SIZE)
                f = Family(0, self.parameter.simulation_time, "family", 'sname', ftype)
                for htype in flist:
                    name = htype.get_name()
                    # name= name.split('<')[0]+"("+ str(id)+")"
                    cname = "check[{0}]".format(name)
                    #Initialize htype
                    htype.set_satisfaction(100)
                    htype.init_seed(htype.get_id()+self.parameter.RANDOM_SEED)
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
        se.get_engine("sname").coupling_relation(None, "start", self.loopback, "start")
        # end of simulation signal
        se.get_engine("sname").insert_external_event("start", None)
        self.READY_SIG.emit()

    def run_simulate(self):
        self.timer += 1
        SystemSimulator().get_engine("sname").simulate(self.timer)
        sim_t = SystemSimulator().get_engine("sname").get_global_time()
        self.progressBar.setValue(sim_t)
        #print(sim_t,file=sys.__stdout__)
        if sim_t / self.parameter.simulation_time >= 1:
            self.worker.stop()
            SystemSimulator().get_engine("sname").destroy_entity()
            SystemSimulator().get_engine("sname").simulation_stop()
            sys.stdout.close()
            sys.stdout= sys.__stdout__
            self.timer = 0
            self.progressBar.setValue(self.parameter.simulation_time)
            if self.parameter.VERBOSE:
                self.RESULT_SIGNAL.emit(self.scenario.N_building  ,self.outputlocation+"/")
            else:
                self.RESULT_SIGNAL.emit(self.scenario.N_building,"output/"+self.scenario.memo + "_" + str(self.parameter.TIME_STDDEV) + "trash" + str(
                self.parameter.TRASH_STDDEV) + "_" + str(self.parameter.GARBAGECAN_SIZE)+self.now)


    def __getattr__(self, attr):
        return getattr(self.obj, attr)