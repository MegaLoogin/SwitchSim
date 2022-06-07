from random import randint
from re import match
import Network


def parse_mac(mac):
    if len(mac) == 17:
        return match('([a-f0-9A-F]{2}:){5}[a-f0-9A-F]{2}', mac) is not None
    else:
        return False


def get_random_mac():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (randint(0, 255), randint(0, 255),
                                              randint(0, 255), randint(0, 255),
                                              randint(0, 255), randint(0, 255))


def get_random_ipv4():
    return [randint(1, 255), randint(1, 255), randint(1, 254), randint(1, 254)]


class Interface:
    def __init__(self, parent_device):
        self.parent_device = parent_device
        self.mac = get_random_mac()
        self.ipv4 = [0, 0, 0, 0]
        self.net_mask = [0, 0, 0, 0]
        self.gateway = [0, 0, 0, 0]
        self.id = Network.Network.id_counter
        Network.Network.id_counter += 1

    def __str__(self):
        return f"ID: {self.id}; MAC: {self.mac}; IPv4: {self.ipv4}; Netmask: {self.net_mask}; Gateway: {self.gateway}"

    def to_dict(self):
        self_dict = self.__dict__
        del self_dict['parent_device']
        return self_dict

    def send_frame(self, frame):
        frame.sender_address = self.mac
        '''if frame.packet.type == "arp":
            frame.packet.sender_MACAddress = self.mac
            frame.packet.sender_IPAddress = self.ipv4'''
        Network.handle_frame(frame)

    def receive_frame(self, frame):
        if frame.packet.type == "arp":
            if frame.target_address == "ff:ff:ff:ff:ff:ff" or frame.target_address == self.mac:
                self.parent_device.on_frame_received(frame, self.mac)
        if frame.packet.type == "ip":
            self.parent_device.on_frame_received(frame, self.mac)
