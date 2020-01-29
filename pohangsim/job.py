import random

from core_component import Statistic
from core_component import HumanType
from core_component import TimeStruct
from core_component import TimeStructContstraintToDay

class AFF(HumanType):
    def __init__(self, _id):
        HumanType.__init__(self, _id)
        pass
        
    def get_type(self):
        return "AFF"

    def get_wakeup(self):
         return TimeStruct(5, 22, Statistic(0, 0, 1))
    
    def get_sleep(self):
        return TimeStruct(22, 14, Statistic(0, 0, 1))

    def get_out(self):
        return TimeStruct(6, 30, Statistic(0, 1, 0.2)) #

    def get_in(self):
        return TimeStruct(17, 0, Statistic(0, 0, 1))
    
    def get_trash(self):
        return 1
        
    def get_satisfaction_func(self, trash):
        if trash >= 0.7:
            return -10
        elif trash < 0.7:
            return 10
        elif trash <= 0:
            return 50

class Housewife(HumanType):
    def __init__(self,_id):
        HumanType.__init__(self ,_id)
        pass
    
    def get_type(self):
        return "Housewife"
        
    def get_wakeup(self):
        return TimeStruct(6, 17, Statistic(0, 0, 1))
    
    def get_sleep(self):
        return TimeStruct(23, 21, Statistic(0, 0, 1))
        
    def get_out(self):
        return TimeStructContstraintToDay(13, 0, Statistic(0, 1, 0.2))
        
    def get_in(self):
        return TimeStruct(15, 0, Statistic(0, 0, 1))
        
    def get_trash(self):
        return 2
 
        
    def get_satisfaction_func(self, trash):
        if trash >= 0.8 :
            return -10
        elif trash <= 0:
            return 20
        elif trash < 0.8:
            return 10

class Student(HumanType):
    def __init__(self,_id):
        HumanType.__init__(self ,_id)
        pass
    
    def get_type(self):
        return "Student"

    def get_wakeup(self):
        return TimeStruct(7,58, Statistic(0, 0, 1))
        
    def get_sleep(self):
        return TimeStruct(24,51, Statistic(0, 0, 1))
  
    def get_out(self):
        return TimeStructContstraintToDay(7,58, Statistic(0, 1, 0.2))

    def get_in(self):
        return TimeStruct(21,00, Statistic(0, 0, 1))

    def get_trash(self):
        return 0.9        

    def get_satisfaction_func(self, trash):
        if trash >= 0.8 :
            return -10
        elif trash <= 0:
            return 20
        elif trash < 0.8:
            return 10

class StudentWithVacation(HumanType):
    def __init__(self,_id):
        HumanType.__init__(self ,_id)
        self.approach = False
        self.count=0
        self.vacation=True
        pass
    
    def get_type(self):
        return "Student"

    def get_wakeup(self):
        return TimeStruct(7,58, Statistic(0, 0, 1))
        
    def get_sleep(self):
        return TimeStruct(24,51, Statistic(0, 0, 1))
  
    def get_out(self):
        if self.approach == False:
            self.approach=True
            return TimeStruct(1464,0,Statistic(0, 0, 1)) # 방학대기 

        else:
            self.count+=1
            
            if self.count >= 122:
                self.vacation=True
                self.approach = False
                self.count=0    
                return TimeStructContstraintToDay(7,58, Statistic(0, 1, 0.2))
            else:
                self.vacation=False
                return TimeStructContstraintToDay(7,58, Statistic(0, 1, 0.2))


    def get_in(self):
        return TimeStruct(21,00, Statistic(0, 0, 1))

    def get_trash(self):
        if self.vacation==True:
            return 0
        else:
            return 2


    def get_satisfaction_func(self, trash):
        if self.vacation == True:            
            return 100
        else:
            if trash >= 0.8 :
                return -10
            elif trash <= 0:
                return 20
            elif trash < 0.8:
                return 10

class Self_employment(HumanType):
    def __init__(self,_id):
        HumanType.__init__(self ,_id)
        pass
    
    def get_type(self):
        return "Self_employment"

    def get_wakeup(self):
        return TimeStruct(6,43, Statistic(0, 0, 1))
        
    def get_sleep(self):
        return TimeStruct(23,54, Statistic(0, 0, 1))
  
    def get_out(self):
        return TimeStructContstraintToDay(6,43, Statistic(0, 1, 0.2))

    def get_in(self):
        return TimeStruct(20,00, Statistic(0, 0, 1))

    def get_trash(self):
        return 1          

    def get_satisfaction_func(self, trash):
        if trash >= 0.5:
            return -10
        elif trash < 0.5:
            return 10
        elif trash == 0:
            return 30

class Blue_collar(HumanType):
    def __init__(self,_id):
        HumanType.__init__(self ,_id)
        pass
    
    def get_type(self):
        return "Blue_collar"

    def get_wakeup(self):
        return TimeStruct(6,22, Statistic(0, 0, 1))
        
    def get_sleep(self):
        return TimeStruct(23,35, Statistic(0, 0, 1))
  
    def get_out(self):
        return TimeStructContstraintToDay(6,22, Statistic(0, 1, 0.2))

    def get_in(self):
        return TimeStruct(17,30, Statistic(0, 0, 1))

    def get_trash(self):
        return 2    

    def get_satisfaction_func(self, trash):
        if trash >= 0.8:
            return -10
        elif trash <= 0:
            return 20
        elif trash < 0.8:
            return 10

class White_collar(HumanType):
    def __init__(self,_id):
        HumanType.__init__(self ,_id)
        pass
    
    def get_type(self):
        return "White_collar"

    def get_wakeup(self):
        return TimeStruct(6,36, Statistic(0, 0, 1))
        
    def get_sleep(self):
        return TimeStruct(23,53, Statistic(0, 0, 1))
  
    def get_out(self):
        return TimeStruct(6,36, Statistic(0, 1, 0.2))

    def get_in(self):
        return TimeStruct(17,30, Statistic(0, 0, 1))

    def get_trash(self):
        return 1          

    def get_satisfaction_func(self, trash):
        if trash >= 0.5:
            return -10
        elif trash < 0.5:
            return 10
        elif trash == 0:
            return 50
    
class Inoccupation(HumanType):
    def __init__(self,_id):
        HumanType.__init__(self ,_id)
        pass
    
    def get_type(self):
        return "Inoccupation"

    def get_wakeup(self):
        return TimeStruct(6,26, Statistic(0, 0, 1))
        
    def get_sleep(self):
        return TimeStruct(23,16, Statistic(0, 0, 1))
  
    def get_out(self):
        return TimeStruct(6,26, Statistic(0, 1, 0.3))

    def get_in(self):
        return TimeStruct(17,00, Statistic(0, 0, 1))

    def get_trash(self):
        return 1          

    def get_satisfaction_func(self, trash):
        if trash >= 0.5:
            return -10
        elif trash < 0.5:
            return 10
        elif trash == 0:
            return 50