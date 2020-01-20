"""
    Light-weighted Simulation Engine
"""


from collections import deque
import heapq
import copy
import time
import datetime

from evsim.definition import *
from evsim.default_message_catcher import *
from evsim.behavior_model import *
from evsim.system_object import *


class SysExecutor(SysObject, BehaviorModel):

    EXTERNAL_SRC = "SRC"
    EXTERNAL_DST = "DST"

    def __init__(self, _time_step, _sim_name='default', _sim_mode='VIRTUAL_TIME'):
        BehaviorModel.__init__(self, _sim_name)

        self.global_time = 0
        self.target_time = 0
        self.time_step = _time_step  # time_step may changed? - cbchoi

        # dictionary for waiting simulation objects
        self.waiting_obj_map = {}
        # dictionary for active simulation objects
        self.active_obj_map = {}
        # dictionary for object to ports
        self.port_map = {}
        #self.port_map_wName = []

        self.min_schedule_item = deque()

        self.sim_init_time = datetime.datetime.now()

#        self.eval_time = 0

        self.register_entity(DefaultMessageCatcher(0, Infinite, "dc", "default"))

        self.simulation_mode = SimulationMode.SIMULATION_IDLE

        # External Interface
        self.input_event_queue = []
        self.output_event_queue = deque()

        # TIME Handling
        self.sim_mode = _sim_mode

        # Learning Module
        self.learn_module = None

    # retrieve global time
    def get_global_time(self):
        return self.global_time

    def register_entity(self, sim_obj):
        if not sim_obj.get_create_time() in self.waiting_obj_map:
            self.waiting_obj_map[sim_obj.get_create_time()] = list()

        self.waiting_obj_map[sim_obj.get_create_time()].append(sim_obj)

    def create_entity(self):
        if len(self.waiting_obj_map.keys()) != 0:
            key = min(self.waiting_obj_map)
            if key <= self.global_time:
                lst = self.waiting_obj_map[key]
                for obj in lst:
                    # print("global:",self.global_time," create agent:", obj.get_obj_name())
                    self.active_obj_map[obj.get_name()] = obj
                    # self.min_schedule_item.append((obj.time_advance() + self.global_time, obj))
                    obj.set_req_time(self.global_time)
                    self.min_schedule_item.append(obj)
                del self.waiting_obj_map[key]

                # select object that requested minimum time
                self.min_schedule_item = deque(sorted(self.min_schedule_item, key=lambda bm: bm.get_req_time()))

    def destroy_entity(self):
        if len(self.active_obj_map.keys()) != 0:
            delete_lst = []
            for agent_name, agent in self.active_obj_map.items():
                if agent.get_destruct_time() <= self.global_time:
                    delete_lst.append(agent)

            for agent in delete_lst:
                print("global:",self.global_time," del agent:", agent.get_name())
                del(self.active_obj_map[agent.get_name()])
                
                port_del_lst = []
                for key, value in self.port_map.items():
                    if value[0][0] is agent:
                        port_del_lst.append(key)

                for key in port_del_lst:
                    del(self.port_map[key])
                self.min_schedule_item.remove(agent)

    def coupling_relation(self, src_obj, out_port, dst_obj, in_port):
        if (src_obj, out_port) in self.port_map:
            self.port_map[(src_obj, out_port)].append((dst_obj, in_port))
        else:
            self.port_map[(src_obj, out_port)] = [(dst_obj, in_port)]
            # self.port_map_wName.append((src_obj.get_name(), out_port, dst_obj.get_name(), in_port))

    '''
    def update_coupling_relation(self):
        self.port_map.clear()

        for i in range(len(self.port_map_wName)):
            src_obj_name = self.port_map_wName[i][0]
            src_obj = None
            # find loaded obj with name
            for q in range(len(self.min_schedule_item)):
                if self.min_schedule_item[q].get_name() == src_obj_name:
                    src_obj = self.min_schedule_item[q]
            out_port = self.port_map_wName[i][1]
            dst_obj_name = self.port_map_wName[i][2]
            dst_obj = None
            for q in range(len(self.min_schedule_item)):
                if self.min_schedule_item[q].get_name() == dst_obj_name:
                    dst_obj = self.min_schedule_item[q]
            in_port = self.port_map_wName[i][3]
            self.port_map[(src_obj, out_port)] = (dst_obj, in_port)
    '''

    def output_handling(self, obj, msg):
        if msg is not None:
            pair = (obj, msg.get_dst())
            if pair not in self.port_map:
                self.port_map[pair] = [(self.active_obj_map["dc"], "uncaught")]

            for port_pair in self.port_map[pair]:
                destination = port_pair
                if destination is None:
                    print("Destination Not Found")
                    raise AssertionError

                if destination[0] is None:
                    self.output_event_queue.append((self.global_time, msg.retrieve()))
                else:
                    # Receiver Message Handling
                    destination[0].ext_trans(destination[1], msg)
                    # Receiver Scheduling
                    # wrong : destination[0].set_req_time(self.global_time + destination[0].time_advance())
                    self.min_schedule_item.remove(destination[0])
                    destination[0].set_req_time(self.global_time)
                    self.min_schedule_item.append(destination[0])
                    #self.min_schedule_item = deque(sorted(self.min_schedule_item, key=lambda bm: bm.get_req_time()))
                    # self.min_schedule_item.pop()
                    # self.min_schedule_item.append((destination[0].time_advance() + self.global_time, destination[0]))

    def init_sim(self):
        self.simulation_mode = SimulationMode.SIMULATION_RUNNING

        if self.active_obj_map is None:
            self.global_time = min(self.waiting_obj_map)

        if not self.min_schedule_item:
            for obj in self.active_obj_map.items():
                if obj[1].time_advance() < 0: # exception handling for parent instance
                    print("You should override the time_advanced function")
                    raise AssertionError

                obj[1].set_req_time(self.global_time)
                self.min_schedule_item.append(obj[1])

    def schedule(self):
        # Agent Creation
        self.create_entity()
        self.handle_external_input_event()

        tuple_obj = self.min_schedule_item.popleft()

        before = time.perf_counter()
        while tuple_obj.get_req_time() <= self.global_time:
            msg = tuple_obj.output()
            if msg is not None:
                self.output_handling(tuple_obj, msg)

            # Sender Scheduling
            tuple_obj.int_trans()
            tuple_obj.set_req_time(self.global_time)
            self.min_schedule_item.append(tuple_obj)

            self.min_schedule_item = deque(sorted(self.min_schedule_item, key=lambda bm: bm.get_req_time()))
            tuple_obj = self.min_schedule_item.popleft()

        self.min_schedule_item.appendleft(tuple_obj)

        # update Global Time
        self.global_time += self.time_step

        after = time.perf_counter()
        if self.sim_mode == "REAL_TIME":
            time.sleep((lambda x: x if x > 0 else 0)(float(self.time_step) - float(after-before)))
        # Agent Deletion
        self.destroy_entity()


    def simulate(self, _time=Infinite):
        # Termination Condition
        self.target_time = self.global_time + _time

        # Get minimum scheduled event
        self.init_sim()

        while self.global_time < self.target_time:
            if not self.waiting_obj_map:
                if self.min_schedule_item[0].get_req_time() == Infinite and self.sim_mode == 'VIRTUAL_TIME' :
                    self.simulation_mode = SimulationMode.SIMULATION_TERMINATED
                    break

            self.schedule()

    def simulation_stop(self):
        self.global_time = 0
        self.target_time = 0
        self.time_step = 1  # time_step may changed? - cbchoi

        # dictionary for waiting simulation objects
        self.waiting_obj_map = {}
        # dictionary for active simulation objects
        self.active_obj_map = {}
        # dictionary for object to ports
        self.port_map = {}
        # self.port_map_wName = []

        self.min_schedule_item = deque()

        self.sim_init_time = datetime.datetime.now()

#        self.eval_time = 0

        self.register_entity(DefaultMessageCatcher(0, Infinite, "dc", "default"))

    # External Event Handling - by cbchoi
    def insert_external_event(self, _port, _msg, scheduled_time=0):
        sm = SysMessage("SRC", _port)
        sm.insert(_msg)
        if _port in self._input_ports:
            heapq.heappush(self.input_event_queue, (scheduled_time + self.global_time, sm))
            if self.simulation_mode != SimulationMode.SIMULATION_IDLE:
                self.handle_external_input_event()
        else:
            # TODO Exception Handling
            pass

    def get_generated_event(self):
        return self.output_event_queue

    def handle_external_input_event(self):
        event_list = [ev for ev in self.input_event_queue if ev[0] <= self.global_time]
        for event in event_list:

            self.output_handling(None, event[1])
            heapq.heappop(self.input_event_queue)

        self.min_schedule_item = deque(sorted(self.min_schedule_item, key=lambda bm: bm.get_req_time()))
        pass

    def handle_external_output_event(self):
        event_lists = copy.deepcopy(self.output_event_queue)
        self.output_event_queue.clear()
        return event_lists

    def is_terminated(self):
        return self.simulation_mode == SimulationMode.SIMULATION_TERMINATED

    def set_learning_module(self, learn_module):
        self.learn_module = learn_module
        pass

    def get_learning_module(self):
        return self.learn_module
"""
    Light-weighted Simulation Engine
"""


from collections import deque
import heapq
import copy
import time
import datetime

from evsim.definition import *
from evsim.default_message_catcher import *
from evsim.behavior_model import *
from evsim.system_object import *


class SysExecutor(SysObject, BehaviorModel):

    EXTERNAL_SRC = "SRC"
    EXTERNAL_DST = "DST"

    def __init__(self, _time_step, _sim_name='default', _sim_mode='VIRTUAL_TIME'):
        BehaviorModel.__init__(self, _sim_name)

        self.global_time = 0
        self.target_time = 0
        self.time_step = _time_step  # time_step may changed? - cbchoi

        # dictionary for waiting simulation objects
        self.waiting_obj_map = {}
        # dictionary for active simulation objects
        self.active_obj_map = {}
        # dictionary for object to ports
        self.port_map = {}
        #self.port_map_wName = []

        self.min_schedule_item = deque()

        self.sim_init_time = datetime.datetime.now()

#        self.eval_time = 0

        self.register_entity(DefaultMessageCatcher(0, Infinite, "dc", "default"))

        self.simulation_mode = SimulationMode.SIMULATION_IDLE

        # External Interface
        self.input_event_queue = []
        self.output_event_queue = deque()

        # TIME Handling
        self.sim_mode = _sim_mode

        # Learning Module
        self.learn_module = None

    # retrieve global time
    def get_global_time(self):
        return self.global_time

    def register_entity(self, sim_obj):
        if not sim_obj.get_create_time() in self.waiting_obj_map:
            self.waiting_obj_map[sim_obj.get_create_time()] = list()

        self.waiting_obj_map[sim_obj.get_create_time()].append(sim_obj)

    def create_entity(self):
        if len(self.waiting_obj_map.keys()) != 0:
            key = min(self.waiting_obj_map)
            if key <= self.global_time:
                lst = self.waiting_obj_map[key]
                for obj in lst:
                    # print("global:",self.global_time," create agent:", obj.get_obj_name())
                    self.active_obj_map[obj.get_name()] = obj
                    # self.min_schedule_item.append((obj.time_advance() + self.global_time, obj))
                    obj.set_req_time(self.global_time)
                    self.min_schedule_item.append(obj)
                del self.waiting_obj_map[key]

                # select object that requested minimum time
                self.min_schedule_item = deque(sorted(self.min_schedule_item, key=lambda bm: bm.get_req_time()))

    def destroy_entity(self):
        if len(self.active_obj_map.keys()) != 0:
            delete_lst = []
            for agent_name, agent in self.active_obj_map.items():
                if agent.get_destruct_time() <= self.global_time:
                    delete_lst.append(agent)

            for agent in delete_lst:
                print("global:",self.global_time," del agent:", agent.get_name())
                del(self.active_obj_map[agent.get_name()])
                
                port_del_lst = []
                for key, value in self.port_map.items():
                    if value[0][0] is agent:
                        port_del_lst.append(key)

                for key in port_del_lst:
                    del(self.port_map[key])
                self.min_schedule_item.remove(agent)

    def coupling_relation(self, src_obj, out_port, dst_obj, in_port):
        if (src_obj, out_port) in self.port_map:
            self.port_map[(src_obj, out_port)].append((dst_obj, in_port))
        else:
            self.port_map[(src_obj, out_port)] = [(dst_obj, in_port)]
            # self.port_map_wName.append((src_obj.get_name(), out_port, dst_obj.get_name(), in_port))

    '''
    def update_coupling_relation(self):
        self.port_map.clear()

        for i in range(len(self.port_map_wName)):
            src_obj_name = self.port_map_wName[i][0]
            src_obj = None
            # find loaded obj with name
            for q in range(len(self.min_schedule_item)):
                if self.min_schedule_item[q].get_name() == src_obj_name:
                    src_obj = self.min_schedule_item[q]
            out_port = self.port_map_wName[i][1]
            dst_obj_name = self.port_map_wName[i][2]
            dst_obj = None
            for q in range(len(self.min_schedule_item)):
                if self.min_schedule_item[q].get_name() == dst_obj_name:
                    dst_obj = self.min_schedule_item[q]
            in_port = self.port_map_wName[i][3]
            self.port_map[(src_obj, out_port)] = (dst_obj, in_port)
    '''

    def output_handling(self, obj, msg):
        if msg is not None:
            pair = (obj, msg.get_dst())
            if pair not in self.port_map:
                self.port_map[pair] = [(self.active_obj_map["dc"], "uncaught")]

            for port_pair in self.port_map[pair]:
                destination = port_pair
                if destination is None:
                    print("Destination Not Found")
                    raise AssertionError

                if destination[0] is None:
                    self.output_event_queue.append((self.global_time, msg.retrieve()))
                else:
                    # Receiver Message Handling
                    destination[0].ext_trans(destination[1], msg)
                    # Receiver Scheduling
                    # wrong : destination[0].set_req_time(self.global_time + destination[0].time_advance())
                    self.min_schedule_item.remove(destination[0])
                    destination[0].set_req_time(self.global_time)
                    self.min_schedule_item.append(destination[0])
                    #self.min_schedule_item = deque(sorted(self.min_schedule_item, key=lambda bm: bm.get_req_time()))
                    # self.min_schedule_item.pop()
                    # self.min_schedule_item.append((destination[0].time_advance() + self.global_time, destination[0]))

    def init_sim(self):
        self.simulation_mode = SimulationMode.SIMULATION_RUNNING

        if self.active_obj_map is None:
            self.global_time = min(self.waiting_obj_map)

        if not self.min_schedule_item:
            for obj in self.active_obj_map.items():
                if obj[1].time_advance() < 0: # exception handling for parent instance
                    print("You should override the time_advanced function")
                    raise AssertionError

                obj[1].set_req_time(self.global_time)
                self.min_schedule_item.append(obj[1])

    def schedule(self):
        # Agent Creation
        self.create_entity()
        self.handle_external_input_event()

        tuple_obj = self.min_schedule_item.popleft()

        before = time.perf_counter()
        while tuple_obj.get_req_time() <= self.global_time:
            msg = tuple_obj.output()
            if msg is not None:
                self.output_handling(tuple_obj, msg)

            # Sender Scheduling
            tuple_obj.int_trans()
            tuple_obj.set_req_time(self.global_time)
            self.min_schedule_item.append(tuple_obj)

            self.min_schedule_item = deque(sorted(self.min_schedule_item, key=lambda bm: bm.get_req_time()))
            tuple_obj = self.min_schedule_item.popleft()

        self.min_schedule_item.appendleft(tuple_obj)

        # update Global Time
        self.global_time += self.time_step

        after = time.perf_counter()
        if self.sim_mode == "REAL_TIME":
            time.sleep((lambda x: x if x > 0 else 0)(float(self.time_step) - float(after-before)))
        # Agent Deletion
        self.destroy_entity()


    def simulate(self, _time=Infinite):
        # Termination Condition
        self.target_time = self.global_time + _time

        # Get minimum scheduled event
        self.init_sim()

        while self.global_time < self.target_time:
            if not self.waiting_obj_map:
                if self.min_schedule_item[0].get_req_time() == Infinite and self.sim_mode == 'VIRTUAL_TIME' :
                    self.simulation_mode = SimulationMode.SIMULATION_TERMINATED
                    break

            self.schedule()

    def simulation_stop(self):
        self.global_time = 0
        self.target_time = 0
        self.time_step = 1  # time_step may changed? - cbchoi

        # dictionary for waiting simulation objects
        self.waiting_obj_map = {}
        # dictionary for active simulation objects
        self.active_obj_map = {}
        # dictionary for object to ports
        self.port_map = {}
        # self.port_map_wName = []

        self.min_schedule_item = deque()

        self.sim_init_time = datetime.datetime.now()

#        self.eval_time = 0

        self.register_entity(DefaultMessageCatcher(0, Infinite, "dc", "default"))

    # External Event Handling - by cbchoi
    def insert_external_event(self, _port, _msg, scheduled_time=0):
        sm = SysMessage("SRC", _port)
        sm.insert(_msg)
        if _port in self._input_ports:
            heapq.heappush(self.input_event_queue, (scheduled_time + self.global_time, sm))
            if self.simulation_mode != SimulationMode.SIMULATION_IDLE:
                self.handle_external_input_event()
        else:
            # TODO Exception Handling
            pass

    def get_generated_event(self):
        return self.output_event_queue

    def handle_external_input_event(self):
        event_list = [ev for ev in self.input_event_queue if ev[0] <= self.global_time]
        for event in event_list:

            self.output_handling(None, event[1])
            heapq.heappop(self.input_event_queue)

        self.min_schedule_item = deque(sorted(self.min_schedule_item, key=lambda bm: bm.get_req_time()))
        pass

    def handle_external_output_event(self):
        event_lists = copy.deepcopy(self.output_event_queue)
        self.output_event_queue.clear()
        return event_lists

    def is_terminated(self):
        return self.simulation_mode == SimulationMode.SIMULATION_TERMINATED

    def set_learning_module(self, learn_module):
        self.learn_module = learn_module
        pass

    def get_learning_module(self):
        return self.learn_module