from Camera import *
from devices.PC import *
from devices.Switch import *
from Connection import *
from Animation import *
import pygame


class Game:
    types = {
        "pc": {
            "size": (50, 50),
            "file_name": "res\\pc.png",
            "object": PC
        },
        "switch": {
            "size": (50, 50),
            "file_name": "res\\switch.png",
            "object": Switch
        },
        "mail_sending": {
            "size": (20, 20),
            "file_name": "res\\mail_sending.png",
            "object": None
        },
        "mail_sendend": {
            "size": (20, 20),
            "file_name": "res\\mail_sended.png",
            "object": None
        },
        "mail_error": {
            "size": (20, 20),
            "file_name": "res\\mail_error.png",
            "object": None
        }
    }

    def __init__(self, window, camera_pos, tps=20):
        self.window = window
        self.camera = Camera(self, camera_pos, 1)
        self.selected_object = "none"

        self.anims = list()
        self.load_images()

        self.objects = list()

        self.buffer_device = None
        self.connections = list()

        self.tps = tps

    def process_tick(self):
        for obj in self.objects:
            obj.tick()

    def load_images(self):
        for tp in self.types:
            self.types[tp]["image"] = pygame.image.load(self.types[tp]["file_name"])

    def add_animation(self, image_type, pos):
        self.anims.append(Animation(self.types[image_type]["size"], self.types[image_type]["image"],
                                    pos, pygame.time.get_ticks(), self))

    def is_selected(self):
        return self.selected_object in self.types.keys()

    def place_object(self, pos):
        if self.is_selected():
            size = self.types[self.selected_object]["size"]
            rect = pygame.Rect((pos[0] - size[0] / 2, pos[1] - size[1] / 2), size)

            if not rect.collidelistall(Object.get_list(self.objects)):
                image = self.types[self.selected_object]["image"]
                self.objects.append(self.types[self.selected_object]["object"](rect, self.window))
                self.objects[-1].load_image(image)

    def make_connection(self, first, second, ports):
        self.connections.append(Connection(first, second, ports))

        first.connections[ports[0]] = self.connections[-1]
        second.connections[ports[1]] = self.connections[-1]

    def get_object(self, point):
        for obj in self.objects:
            if obj.rect.collidepoint(point):
                return obj
        return None
