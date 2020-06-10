#GUI lib import
from PySide2.QtCore import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from building_dialog import BuildingTypeManager
from control_box import controlBox
# matplot
from matplotlib.backends.backend_qt5agg import FigureCanvas
#from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from scenario_editor import ScenarioClass, new_scenario_GUI, load_scenario_GUI, save_scenario_GUI

import pandas as pd

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
        self.fig= Figure(figsize=(5, 3))
        self.dynamic_canvas = FigureCanvas(self.fig)
        #self.toolbar = NavigationToolbar(self.dynamic_canvas, self.obj)
        self.dynamic_canvas.setVisible(False)
        self.figindex=0
        self.length=0
        self.data=None
        #self.dynamic_canvas.figure.tight_layout()+
        self.resultLayout.addWidget(self.dynamic_canvas)
        self._dynamic_ax = self.dynamic_canvas.figure.subplots()
        self.plusFig.setVisible(False)
        self.minusFig.setVisible(False)
        self.plusFig.clicked.connect(self.nextfig)
        self.minusFig.clicked.connect(self.prevfig)

    def __getattr__(self, attr):
        return getattr(self.obj, attr)

    def show(self):
        self.obj.show()
    def nextfig(self):
        if self.figindex == self.length-1:
            self.figindex = 0
        else:
            self.figindex += 1
        self.show_plot()
        pass

    def prevfig(self):
        if self.figindex==0:
            self.figindex=self.length-1
        else:
            self.figindex-=1
        self.show_plot()
        pass

    def show_plot(self):
        self._dynamic_ax.clear()
        if self.figindex==0:
            #truckcsv, main
            truckcsv=self.data[0]
            unzipped = list(zip(*truckcsv))
            self._dynamic_ax.bar(unzipped[0], unzipped[4])
            self._dynamic_ax.set_title('Truck Data')
        elif self.figindex==1:
            if self.data[1] == []:
                self._dynamic_ax.bar(['Student', 'Homemaker', "Blue_Collar"], [0, 0, 0])
                self._dynamic_ax.set_title('Total reports')
            else:
                nonver = self.data[1]
                unzipped = list(zip(*nonver))
                self._dynamic_ax.bar(unzipped[0], unzipped[1])
                self._dynamic_ax.set_title('Total reports')
        elif self.figindex>1:
            can = self.data[self.figindex]
            unzipped = list(zip(*can))
            if len(unzipped) != 0:
                if int(self.figindex % 2) == 1:
                    self._dynamic_ax.bar(unzipped[0], unzipped[2])
                    #satisfaction
                    self._dynamic_ax.set_title('Garbagecan Trash#' + str(int(self.figindex - 1)/2))
                else:
                    #trash
                    self._dynamic_ax.bar(unzipped[0], unzipped[2])
                    self._dynamic_ax.set_title('Satisfaction  Can #' + str(int(self.figindex/2)))
            else:
                if int(self.figindex % 2) == 1:
                    self._dynamic_ax.set_title('No reports for can' + str(int(self.figindex - 1)/2))
                else:
                    self._dynamic_ax.set_title('No reports for Checker' + str(int(self.figindex/2)))


        self.dynamic_canvas.figure.canvas.draw()
        self.obj.repaint()


    @Slot(list)
    def _update_canvas(self, points):
        self._dynamic_ax.clear()
        self.length=len(points)
        if self.length == 1:
            self.plusFig.setVisible(False)
            self.minusFig.setVisible(False)
            nonver=points[-1]
            if nonver!=[]:
                unzipped = list(zip(*nonver))
                self.x_data, self.y_data = unzipped[0], unzipped[1]
                self._dynamic_ax.bar(unzipped[0], unzipped[1])
                self._dynamic_ax.set_title('Total reports')
            else:#complain이 없을때
                self._dynamic_ax.bar(['Student','Homemaker',"Blue_Collar"],[0,0,0])
                self._dynamic_ax.set_title('Total reports')
        elif self.length >1:
            self.plusFig.setVisible(True)
            self.minusFig.setVisible(True)
            if points[1]==[]:
                self._dynamic_ax.bar(['Student', 'Homemaker', "Blue_Collar"], [0, 0, 0])
                self._dynamic_ax.set_title('Total reports')
            else:
                ver=points[1]
                unzipped = list(zip(*ver))
                self._dynamic_ax.bar(unzipped[0], unzipped[1])
                self._dynamic_ax.set_title('Total reports')
        self.figindex=1
        self.data=points
        self.dynamic_canvas.setVisible(True)
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

        #controlbox
        #Simulate 버튼 클릭시
        self.controlbox.SimulateButton.clicked.connect(self.ScenarioListControl.send_scenario) #scenario list 전달
        self.ScenarioListControl.SCENARIO_SIGNAL.connect(self.controlbox.prepare_data) #parameter 읽기 -> timerstart
        self.controlbox.READY_SIG.connect(self.controlbox.timer_start)
        # simulation이 끝나면 결과
        self.controlbox.RESULT_SIGNAL.connect(self.output.show_result) #알림창 띄우기
        self.output.DATA_SIG.connect(self.MatplotResult._update_canvas)
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
    DATA_SIG=Signal(list)
    def __init__(self, _parent=None):
        super(OutputManager,self).__init__(_parent)
        self.obj=_parent
        self.dialog=None

    @Slot()
    def show_result(self, Ncan,fileurl):
        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText("Simulation is finished")
        msg.exec_()
        loadedlist = []
        if fileurl.startswith("output"):
            try:
                log = pd.read_csv(fileurl + ".log",index_col=False, names=['1', '2', '3', '4', '5','6'])
                df = pd.DataFrame(index=range(0, 3), columns=['job', 'reports'])
                df['job'] =  log['1'][0], log['3'][0], log['5'][0]
                df['reports'] =log['2'][0], log['4'][0], log['6'][0]
                loadedlist.append(df.values.tolist())

            except:
                loadedlist.append([])
        else:
            truck = pd.read_csv(fileurl + "truck.csv",
                                names=['time', 'Visit order', 'Building number', 'Current Truck Storage',
                                       'Total Accumulated Waste'])
            loadedlist.append(truck.values.tolist())
            try:
                log = pd.read_csv("output/"+fileurl.strip("/") + ".log", index_col=False, names=['1', '2', '3', '4', '5', '6'])
                df = pd.DataFrame(index=range(0, 3), columns=['job', 'reports'])
                df['job'] = log['1'][0], log['3'][0], log['5'][0]
                df['reports'] = log['2'][0], log['4'][0], log['6'][0]
                loadedlist.append(df.values.tolist())
            except:
                loadedlist.append([])
            for i in range(Ncan):
                df_can = pd.read_csv(fileurl + "can_outputgc["+str(i)+"].csv")
                df_can_check = pd.read_csv(fileurl + "can_outputgc["+str(i)+"]_checker.csv")
                loadedlist.append(df_can.values.tolist())
                loadedlist.append(df_can_check.values.tolist())

        self.DATA_SIG.emit(loadedlist)

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


