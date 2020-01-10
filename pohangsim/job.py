x

        self.stat = stat

    def get_unit_time(self):
        delta = self.stat.get_delta()
        return self.hour + float(self.minute)/60 + delta
        
        
class HumanType(object):
    def __init__(self, _type, _wakeup, _sleep, _out, _in, _trash):
        self.type = _type
        self.wakeup = _wakeup
        self.sleep = _sleep
        self.b_out =_out
        self.b_in = _in
        self.trash = _trash
        
        
    def get_type(self):
        return self.type

    def get_wakeup(self):
        # random
        return self.wakeup
    
    def get_sleep(self):
        return self.sleep

    def get_out(self):
        return self.b_out

    def get_in(self):
        return self.b_in
        
    def get_trash(self):
        return self.trash



class AFF(object):
    @staticmethod
    def get_type():
        return "AFF"
        
    @staticmethod
    def get_wakeup_time():
        return TimeStruct(5, 22, Statistic(0, 0, 1))
    
    @staticmethod    
    def get_sleep_time():
        return TimeStruct(22, 14, Statistic(0, 0, 1))
        
    @staticmethod
    def get_out_time():
        return TimeStruct(1, 0, Statistic(0, 0, 1))
        
    @staticmethod
    def get_in_time():
        return TimeStruct(17, 0, Statistic(0, 0, 1))
        
    @staticmethod
    def get_trash():
        return 0.9
        
'''
class Self_employment(object):
    @staticmethod
    def get_wakeup_time():
        return TimeStruct(6,43)
        
    @staticmethod        
    def get_sleep():
        return TimeStruct(23,54)
  
    @staticmethod        
    def get_out_time():
        return TimeStruct(6,43)
        
    @staticmethod
    def get_in_time():
        return TimeStruct(20,00)

    @staticmethod
    def get_trash():
        return 0.9

class Blue_collar(object):
    @staticmethod
    def get_wakeup_time():
        return TimeStruct(6, 22, Statistic(0, 0, 1))
    
    @staticmethod    
    def get_sleep_time():
        return TimeStruct(23, 35, Statistic(0, 0, 1))
        
    @staticmethod
    def get_out_time():
        return TimeStruct(6, 22, Statistic(0, 0, 1))
        
    @staticmethod
    def get_in_time():
        return TimeStruct(17, 30, Statistic(0, 0, 1))
        
    @staticmethod
    def get_trash():
        return 0.9
    
class White_collar(object):
    @staticmethod
    def get_wakeup_time():
        return TimeStruct(6, 36, Statistic(0, 0, 1))
    
    @staticmethod    
    def get_sleep_time():
        return TimeStruct(23, 53, Statistic(0, 0, 1))
        
    @staticmethod
    def get_out_time():
        return TimeStruct(6, 36, Statistic(0, 0, 1))
        
    @staticmethod
    def get_in_time():
        return TimeStruct(17, 30, Statistic(0, 0, 1))
        
    @staticmethod
    def get_trash():
        return 0.9

class White_collar():
    wakeup='6:36:00'
    sleep='23:53:00'
    come_out='6:36:00'
    come_in='18:50'
    


class Housewife():
    wakeup='6:17:00'
    sleep='23:21:00'
    come_out='13:00:00'
    come_in='15:00:00'
    


class Student(object):
    @staticmethod
    def get_wakeup_time():
        return TimeStruct(7,58)
        
    @staticmethod        
    def get_sleep():
        return TimeStruct(24,51)
  
    @staticmethod        
    def get_out_time():
        return TimeStruct(7,58)
        
    @staticmethod
    def get_in_time():
        return TimeStruct(21,00)

    @staticmethod
    def get_trash():
        return 0.9
    
class Inoccupation(object):
    @staticmethod
    def get_wakeup_time():
        return TimeStruct(6,26)
        
    @staticmethod        
    def get_sleep():
        return TimeStruct(23,16)
  
    @staticmethod        
    def get_out_time():
        return TimeStruct(6,26)
        
    @staticmethod
    def get_in_time():
        return TimeStruct(17,00)

    @staticmethod
    def get_trash():
        return 0.9


def random_job():
    human=random.choice([AFF(),Self_employment(),White_collar(),Blue_collar(),Housewife(),Student(),Inoccupation()])
'''