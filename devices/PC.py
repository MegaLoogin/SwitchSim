import Network
from packet_types.ICMP import ICMP
from proto.Object import *
from Network import *
from packet_types.ARP import ARP
from Frame import Frame
from proto.Interface import get_random_ipv4
import time


class PC(Object):
    def __init__(self, int_count):
        super().__init__()
        self.arp_table = list()

        for i in range(int_count):
            inter = Interface(self)
            inter.ipv4 = get_random_ipv4()
            add_interface(inter)
            self.interfaces.append(inter)

    def __str__(self):
        return f"ID: {self.id}; Type: {type(self).__name__}"

    def to_dict(self):
        self_dict = self.__dict__
        self_dict['class'] = type(self).__name__
        for i in range(len(self.interfaces)):
            self_dict["interfaces"][i] = self.interfaces[i].to_dict()
        return self_dict

    def get_arp_table(self):
        for i in range(len(self.interfaces)):
            self.send_frame(i, Frame("", "ff:ff:ff:ff:ff:ff", ARP("", "ff:ff:ff:ff:ff:ff", [], [])))

    def get_port(self, mac):
        for i in range(len(self.interfaces)):
            if mac == self.interfaces[i].mac:
                return i
        return -1

    def get_mac_by_ip(self, ip):
        for arp in self.arp_table:
            if arp[1] == ip:
                return arp[0]
        return ""

    def send_icmp(self, port, ip, data):
        mac = self.get_mac_by_ip(ip)
        if mac == "":
            self.get_arp_table()
            mac = self.get_mac_by_ip(ip)
        self.send_frame(port, Frame("", mac, ICMP(self.interfaces[port].ipv4, ip, data)))

    def send_frame(self, port, frame):
        if frame.packet.type == "arp": frame.packet.sender_MACAddress = self.interfaces[port].mac
        frame.packet.sender_IPAddress = self.interfaces[port].ipv4
        self.interfaces[port].send_frame(frame)

    def on_frame_received(self, frame, self_mac):
        # time.sleep(0.15)
        port = self.get_port(self_mac)
        print(frame)

        if frame.packet.type == "arp":
            change = True
            for i in range(len(self.arp_table)):
                if self.arp_table[i][0] == frame.packet.sender_MACAddress:
                    if not self.arp_table[i][1] == frame.packet.sender_IPAddress:
                        self.arp_table[i] = (frame.packet.sender_MACAddress, frame.packet.sender_IPAddress)
                    change = False
                    break
            if change:
                self.arp_table.append((frame.packet.sender_MACAddress, frame.packet.sender_IPAddress))

        if frame.packet.type == "ip":
            if frame.packet.data_type == "icmp":
                if frame.packet.data == "ping":
                    self.send_icmp(port, frame.packet.sender_IPAddress, "pong")
                if frame.packet.data == "pong":
                    print(f"Response from {frame.packet.sender_IPAddress}")

        if frame.packet.type == "arp":
            if frame.packet.target_MACAddress == "ff:ff:ff:ff:ff:ff":
                self.send_frame(port, Frame("", frame.sender_address, ARP("", frame.packet.sender_MACAddress, self.interfaces[port].ipv4, frame.packet.sender_IPAddress)))

