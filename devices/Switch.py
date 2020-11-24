from Frame import *
from Object import *


class Switch(Object):
    def __init__(self, obj_rect, window):
        super().__init__(obj_rect, window)
        self.type = "switch"
        self.max_connections = 5
        self.connections = [None] * self.max_connections

        self.mac = self.get_random_mac()

        self.responses = [None] * self.max_connections
        self.requests = [None] * self.max_connections

        self.macs_table = [None] * self.max_connections

        self._gui = dict()

    def show_gui(self):
        pass

    def add_to_table(self, port, mac):
        if self.macs_table[port] is None:
            if not self.macs_table[port] == mac:
                self.macs_table[port] = mac

    def get_port_by_mac(self, mac):
        for port, m in enumerate(self.macs_table):
            if m == mac:
                return port
        return -1

    def tick(self):
        for port, req in enumerate(self.requests):
            if req is not None and self.connections[port] is not None:
                self.connections[port].send(req, self)
        for port, res in enumerate(self.responses):
            if res is not None:
                print("\nSWITCH:\nPort:", port, res)

                self.add_to_table(port, res.sender)

                if not res.type == "mac":
                    reciever = self.get_port_by_mac(res.reciever)

                    if reciever == -1:
                        for p, v in enumerate(self.connections):
                            if not p == port:
                                self.requests[p] = Frame("mac", self.mac, "", self.mac)
                            else:
                                self.requests[p] = Frame("error", "MAC not found", "", self.mac)
                    else:
                        self.requests[reciever] = res

                print(self.macs_table)
                self.responses[port] = None
