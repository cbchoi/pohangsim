from abc import *

class Statistic(object):
    def __init__(self, seed, mean, stddev):
        self.mean = mean
        self.stddev = stddev
        self.rseed = seed
        
    def get_mean(self):
        return self.mean
        
    def get_stddev(self):
        return self.get_stddev()
    
    def get_seed(self):
        return self.rseed
        
    def get_delta(self):
        #val = random.randint(-5, 5)/10
        val = 0
        # calculate delta
        return val
        
class TimeStruct(object):
    def __init__(self, hour, minute, stat):
        self.hour = hour
        self.minute = minute
        self.stat = stat

    def get_unit_time(self):
        delta = self.stat.get_delta()
        return self.hour + float(self.minute)/60 + delta
        
        
class HumanType(object):
    def __init__(self, _id):
        self.h_id = _id
        pass
    
    def get_name(self):
        return '{0}_{1}'.format(self.get_type(), self.h_id)
        
    def get_id(self):
        return self.h_id
        
    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def get_wakeup(self):
        pass
    
    @abstractmethod
    def get_sleep(self):
        pass

    @abstractmethod
    def get_out(self):
        pass

    @abstractmethod
    def get_in(self):
        pass
        
    @abstractmethod
    def get_trash(self):
        pass
        
    @abstractmethod
    def get_satisfaction_func(self, trash):
        pass
        
        
class FamilyType(object):
    def __init__(self, garbage_size):
        self.family_member = []
        self.garbage_storage_size = garbage_size
        self.current_storage_size = 0
        
    def register_member(self, htype):
        self.family_member.append(htype)
    
    def stack_garbage(self, amount):
        self.current_storage_size += amount
    
    def should_empty(self):
        if self.garbage_storage_size > self.current_storage_size:
            return False
        else:
            return True

    def is_flush(self, member):
        if member == self.select_member().get_id():
            return True
        else:
            return False
    
    def select_member(self):
        # random
        # 지정
        # ... 
        return self.family_member[0]
    
    def get_stack_amount(self):
        return self.current_storage_size
        
    def empty_stack(self):
        self.current_storage_size = 0