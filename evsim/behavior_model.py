# from system_entity.attribute import *
from collections import OrderedDict


class BehaviorModel(object):
    def __init__(self, _name=""):
        # super(ModelBehaviorAttribute, self).__init__("BEHAVIOR")
        self._name = _name
        self._states = {}
        # Input Ports Declaration
        self._input_ports = []
        # Output Ports Declaration
        self._output_ports = []

        self.external_transition_map_tuple = {}
        self.external_transition_map_state = {}
        self.internal_transition_map_tuple = {}
        self.internal_transition_map_state = {}

    def set_name(self, _name):
        self._name = _name

    def get_name(self):
        return self._name

    def insert_input_port(self, port):
        self._input_ports.append(port)

    def retrieve_input_ports(self):
        return self._input_ports

    def insert_output_port(self, port):
        self._output_ports.append(port)

    def retrieve_output_ports(self):
        return self._output_ports

    def insert_state(self, name, deadline="inf"):
        # TODO: Exception Handling
        # TA < 0
        # Duplicated State
        self._states[name] = float(deadline)

    def retrieve_states(self):
        return self._states

    def find_state(self, name):
        return name in self._states

    def insert_external_transition(self, pre_state, event, post_state):
        self.external_transition_map_tuple[(pre_state, event)] = post_state
        if pre_state in self.external_transition_map_state:
            self.external_transition_map_state[pre_state].append(event, post_state)
        else:
            self.external_transition_map_state[pre_state] = [(event, post_state)]

    def retrieve_external_transition(self, pre_state):
        return self.external_transition_map_state[pre_state]

    def retrieve_next_external_state(self, pre_state, event):
        return self.external_transition_map_tuple[(pre_state, event)]

    def find_external_transition(self, pre_state):
        return pre_state in self.external_transition_map_state

    def insert_internal_transition(self, pre_state, event, post_state):
        self.internal_transition_map_tuple[(pre_state, event)] = post_state
        if pre_state in self.internal_transition_map_state:
            self.internal_transition_map_state[pre_state].append(event, post_state)
        else:
            self.internal_transition_map_state[pre_state] = [(event, post_state)]

    def retrieve_internal_transition(self, pre_state):
        return self.internal_transition_map_state[pre_state]

    def retrieve_next_internal_state(self, pre_state, event):
        return self.internal_transition_map_tuple[(pre_state, event)]

    def find_internal_transition(self, pre_state):
        return pre_state in self.internal_transition_map_state

    def serialize(self):
        json_obj = OrderedDict()
        json_obj["name"] = self._name
        json_obj["states"] = self._states
        json_obj["input_ports"] = self.retrieve_input_ports()
        json_obj["output_ports"] = self.retrieve_output_ports()
        json_obj["external_trans"] = self.external_transition_map_state
        json_obj["internal_trans"] = self.internal_transition_map_state
        return json_obj

    def deserialize(self, json):
        self._name = json["name"]
        for k, v in json["states"].items():
            self.insert_state(k, v)

        # Handle In ports
        for port in json["input_ports"]:
            self.insert_input_port(port)

        # Handle out ports
        for port in json["output_ports"]:
            self.insert_output_port(port)

        # Handle External Transition
        for k, v in json["external_trans"].items():
            for ns in v:
                self.insert_external_transition(k, ns[0], ns[1])

        # Handle Internal Transition
        for k, v in json["internal_trans"].items():
            for ns in v:
                self.insert_internal_transition(k, ns[0], ns[1])
