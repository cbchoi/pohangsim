from evsim.definition import CoreModel
from collections import OrderedDict

class StructuralModel(CoreModel):
    def __init__(self, _name=""):
        super(StructuralModel, self).__init__(_name)
        self._name = _name
        self._models = []
        # Input Ports Declaration
        self._input_ports = []
        # Output Ports Declaration
        self._output_ports = []

        self.external_input_coupling_map = {}
        self.external_output_coupling_map = {}
        self.internal_coupling_map = {}

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

    def insert_model(self, model):
        self._models.append(model)

    def retrieve_models(self):
        return self._models

    def insert_external_input_coupling(self, src_port, internal_model, dst_port):
        self.external_input_coupling_map[(None, src_port)] = (internal_model, dst_port)
        pass

    def insert_external_output_coupling(self, internal_model, src_port, dst_port):
        self.external_output_coupling_map[(internal_model, src_port)] = (None, dst_port)
        pass

    def insert_internal_coupling(self, src_model, src_port, dst_model, dst_port):
        self.internal_coupling_map[(src_model, src_port)] = (dst_model, dst_port)
        pass

    def retrieve_external_input_coupling(self):
        return self.external_input_coupling_map

    def retrieve_external_output_coupling(self):
        return self.external_output_coupling_map

    def retrieve_internal_coupling(self):
        return self.internal_coupling_map

'''
TODO: serialize using dill
    def serialize(self):
        json_obj = OrderedDict()
        json_obj["name"] = self._name
        json_obj["models"] = self._models
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
'''