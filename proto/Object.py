from proto.Interface import *
from Network import *


class Object:
    def __init__(self):
        self.interfaces = []
        self.id = Network.id_counter
        Network.id_counter += 1

    def __str__(self):
        return ""

    def to_json(self):
        return ""
