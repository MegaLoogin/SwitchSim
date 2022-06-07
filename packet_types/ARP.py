from packet_types.Packet import Packet


class ARP(Packet):
    def __init__(self, sender_MACAddress, target_MACAddress, sender_IPAddress: list, target_IPAddress: list):
        super().__init__("arp")
        self.sender_MACAddress = sender_MACAddress
        self.target_MACAddress = target_MACAddress
        self.sender_IPAddress = sender_IPAddress
        self.target_IPAddress = target_IPAddress

    def __str__(self):
        return f"PacketType: {self.type}; Sender: {self.sender_MACAddress}; Target: {self.target_MACAddress}; SenderIP: {self.sender_IPAddress}; TargetIP: {self.target_IPAddress}"
