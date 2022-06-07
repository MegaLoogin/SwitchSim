from proto.Object import *
from Network import *
from packet_types.ARP import ARP
from Frame import Frame
import time


class Switch(Object):
    def __init__(self, int_count):
        super().__init__()
        self.mac_table = list()
        for i in range(int_count):
            inter = Interface(self)
            add_interface(inter)
            self.interfaces.append(inter)
            self.mac_table.append("")

    def __str__(self):
        return f"ID: {self.id}; Type: {type(self).__name__}"

    def to_dict(self):
        self_dict = self.__dict__
        self_dict['class'] = type(self).__name__
        for i in range(len(self.interfaces)):
            self_dict["interfaces"][i] = self.interfaces[i].to_dict()
        return self_dict

    def send_frame(self, port, frame):
        frame.sender_address = self.interfaces[port].mac
        self.interfaces[port].send_frame(frame)

    def get_port(self, mac):
        for i in range(len(self.interfaces)):
            if mac == self.interfaces[i].mac:
                return i
        return -1

    def on_frame_received(self, frame, self_mac):
        # time.sleep(0.15)
        print(frame)
        port = self.get_port(self_mac)
        self.mac_table[port] = frame.sender_address
        if frame.packet.type == "ip":
            for i in range(len(self.mac_table)):
                if self.mac_table[i] == frame.target_address:
                    self.send_frame(i, Frame("", self.mac_table[i], frame.packet))
        if frame.packet.type == "arp":
            if frame.packet.target_MACAddress == "ff:ff:ff:ff:ff:ff":
                self.send_frame(port, Frame("", frame.sender_address, ARP(self_mac, frame.packet.sender_MACAddress, [], frame.packet.sender_IPAddress)))
                for i in range(len(self.interfaces)):
                    if i == port:
                        continue
                    if self.mac_table[i] == "":
                        self.send_frame(i, Frame("", "ff:ff:ff:ff:ff:ff", ARP(self_mac, "ff:ff:ff:ff:ff:ff", [], [])))
                    else:
                        self.send_frame(i, Frame("", self.mac_table[i], frame.packet))
            elif not frame.packet.target_MACAddress == self_mac:
                for i in range(len(self.mac_table)):
                    if self.mac_table[i] == frame.packet.target_MACAddress:
                        self.send_frame(i, Frame("", self.mac_table[i], frame.packet))

        #print("MAC Table:", self.mac_table)
