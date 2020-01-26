from abc import *
#import numpy as np
import random

class Statistic(object):
    def __init__(self, seed, mean, stddev):
        self.mean = mean
        self.stddev = stddev
        self.rseed = seed

    def get_mean(self):
        return self.mean
        
    def get_stddev(self):
        return self.stddev
    
    def get_seed(self):
        return self.rseed
        
    def get_delta(self):
        #val=np.random.normal(self.mean,self.stddev)
        # calculate delta
        val = random.normalvariate(self.mean, self.stddev)
        return val
        
class TimeStruct(object):
    def __init__(self, hour, minute, stat):
        self.hour = hour
        self.minute = minute
        self.stat = stat

    def get_unit_time(self):
        delta = self.stat.get_delta()
        return self.hour + float(self.minute)/60 + delta
        
class TimeStructContstraintToDay(TimeStruct):
    def __init__(self, hour, minute, stat):
        super(TimeStructContstraintToDay, self).__init__(hour, minute, stat)
        self.prev_time = 0

    def get_unit_time(self):
        delta = self.stat.get_delta()

        prev_time = self.prev_time
        cur_time = self.hour + float(self.minute)/60 + delta
        prev_time = 24 - cur_time
        return prev_time + cur_time

class HumanType(object):
    def __init__(self, _id):
        self.h_id = _id
        self.satisfaction = 100
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

    def get_satisfaction(self):
        return self.satisfaction 
        

import random

class FamilyType(object):
    def __init__(self, garbage_size):
        self.family_member = {}
        self.garbage_storage_size = garbage_size
        self.current_storage_size = 0
        
    def register_member(self, htype):
        self.family_member[htype] = 0

    def get_members(self):
        return self.family_member
    
    def stack_garbage(self, amount):
        self.current_storage_size += amount
    
    def should_empty(self):
        if self.garbage_storage_size > self.current_storage_size:
            return False
        else:
            return True

    def is_flush(self, member):
        if member == self.select_member():
            return True
        else:
            return False
    
    def select_member(self):
        # random
        # 지정
        # ... 
        lst = list(self.family_member.keys())
        #random.shuffle(lst)
        return lst[0]
    
    def get_stack_amount(self):
        return self.current_storage_size
        
    def empty_stack(self):
        self.current_storage_size = 0
        for k in self.family_member.keys():
            self.family_member[k] = 0