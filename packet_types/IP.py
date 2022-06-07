from packet_types.Packet import Packet


class IP(Packet):
    def __init__(self, sender_IPAddress: list, target_IPAddress: list, data_type, data):
        super().__init__("ip")
        self.sender_IPAddress = sender_IPAddress
        self.target_IPAddress = target_IPAddress
        self.data_type = data_type
        self.data = data

    def __str__(self):
        return f"PacketType: {self.type}; Sender: {str(self.sender_IPAddress)};" \
               f" Target: {str(self.target_IPAddress)}; DataType: {self.data_type}; Data: {self.data}"
