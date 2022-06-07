from packet_types.IP import IP


class ICMP(IP):
    def __init__(self, sender_IPAddress, target_IPAddress, data):
        super().__init__(sender_IPAddress, target_IPAddress, "icmp", data)
