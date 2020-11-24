class Connection:
    def __init__(self, first_device, second_device, ports):
        self.devices = list()
        self.devices.append(first_device)
        self.devices.append(second_device)
        self.ports = ports

    def get_line(self):
        rect_f = self.devices[0].rect
        rect_s = self.devices[1].rect
        return (rect_f.x + rect_f.w / 2, rect_f.y + rect_f.h / 2), (rect_s.x + rect_s.w / 2, rect_s.y + rect_s.h / 2)

    def send(self, message, sender_object):
        endpoint = self.get_endpoint(sender_object)
        self.devices[0].window.game.add_animation("mail_sending",
                                                  (sender_object.rect.topleft, endpoint.rect.topleft))
        endpoint.responses[self.get_endpoint_port(sender_object)] = message
        sender_object.confirming_frame = sender_object.requests[self.get_device_port(sender_object)]
        sender_object.confirming = True
        sender_object.requests[self.get_device_port(sender_object)] = None

    def disconnect_from_all(self):
        self.devices[0].connections[self.ports[0]] = None
        self.devices[1].connections[self.ports[1]] = None

    def get_device_port(self, device):
        return self.ports[0] if device == self.devices[0] else self.ports[1]

    def get_endpoint(self, startpoint):
        return self.devices[0] if startpoint == self.devices[1] else self.devices[1]

    def get_endpoint_port(self, startpoint):
        return self.ports[0] if startpoint == self.devices[1] else self.ports[1]
