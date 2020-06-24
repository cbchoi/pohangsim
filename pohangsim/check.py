from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *
from experiments.UI.config import *
from pohangsim.core_component import Statistic

class Check(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, htype):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("CHECK", 0)
        self.insert_state("REPORT",0)
        
        self.insert_input_port("request")
        self.insert_input_port("checked") # from garbage can
        
        self.insert_output_port("check") # to garbage can
        self.insert_output_port("gov_report")

        self.stat=Statistic(RANDOM_SEED,20,4)  #Satisfaction mean and stddev
        self.htype = htype
#        self.satis_func = satis_func
#        self.satisfaction = 100
#        self.hid = hid
        #init seed
        self.htype.out_time.stat.init_seed()
        self.htype.trash.init_seed()
    def get_satis(self, trash):
        if trash > 0.5:
            return -10
        else:
            return 10
        pass
        
    def ext_trans(self,port, msg):
        if self.htype.is_vacation():
            self.htype.satisfaction=None
            pass
        else:
            if port == "request":
                self._cur_state = "CHECK"
            
            if port == "checked":
                if self.htype.satisfaction==None:
                    self.htype.satisfaction=100
                    self.htype.satisfaction += self.htype.get_satisfaction_func(msg.retrieve()[0])
                else:                            
                #    self.htype.satisfaction += self.htype.get_satisfaction_func(msg.retrieve()[0])
                    self.htype.satisfaction += self.get_satis(msg.retrieve()[0])

                
                if self.htype.satisfaction >= 100:
                    self.htype.satisfaction = 100
                if self.htype.satisfaction < 0:
                    self.htype.satisfaction += self.stat.get_delta()
                    self._cur_state = "REPORT"
                #print(self.htype.)
                #print(SystemSimulator().get_engine("sname").get_global_time(),"[check] "+self.get_name() + ":" + str(self.htype.satisfaction))

    def output(self):
        if self._cur_state=="CHECK":
            if self.htype.is_vacation():
                self.htype.satisfaction=None
                return None
            else:
                msg = SysMessage(self.get_name(), "check")
                msg.insert(self.htype)
                return msg
            
        if self._cur_state == "REPORT":
            #print('[check]#')
            msg = SysMessage(self.get_name(), "gov_report")
            msg.insert(self.htype)
            return msg
            
        return None

    def int_trans(self):
        if self._cur_state == "CHECK":
            self._cur_state = "IDLE"
        elif self._cur_state=="REPORT":
            self._cur_state = "IDLE"
