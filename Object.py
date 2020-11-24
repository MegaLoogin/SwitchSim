import random
import re


class Object:
    def __init__(self, rect, window):
        self.connections = None
        self.window = window
        self.rect = rect
        self.image = None
        self.selected = False
        self.ui_window = None

        self.confirming_frame = None
        self.confirming = False
        self.wait_cycle = 0
        self.max_wait_cycles = 4

        self.max_connections = 0

    @staticmethod
    def get_list(objs):
        ls = list()
        for obj in objs:
            ls.append(obj)
        return ls

    def remove_connections(self):
        for con in self.connections:
            for i, gcon in enumerate(self.window.game.connections):
                if con == gcon:
                    self.window.game.connections[i].disconnect_from_all()

                    self.window.game.connections.pop(i)

    def get_free_port(self):
        for p in range(self.max_connections):
            if self.connections[p] is None:
                return p
        return -1

    @staticmethod
    def get_random_mac():
        return "%02x:%02x:%02x:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255),
                                                  random.randint(0, 255), random.randint(0, 255),
                                                  random.randint(0, 255), random.randint(0, 255))

    @staticmethod
    def parse_mac(mac):
        if len(mac) == 17:
            return re.match('([a-f0-9A-F]{2}:){5}[a-f0-9A-F]{2}', mac) is not None
        else:
            return False

    def load_image(self, image):
        self.image = image
