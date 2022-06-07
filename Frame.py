class Frame(object):
    def __init__(self, sender_address, target_address, packet):
        self.sender_address = sender_address  # mac
        self.target_address = target_address  # mac
        self.packet = packet

    def __str__(self):
        return f"Sender: {self.sender_address}; Target: {self.target_address}; Packet: [ {str(self.packet)} ]"
