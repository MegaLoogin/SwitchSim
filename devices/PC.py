from Object import *
from pygame import Rect
from Frame import *
import pygame_gui
from pygame_gui.elements import *


class PC(Object):
    def __init__(self, obj_rect, window):
        super().__init__(obj_rect, window)
        self.pos = (0, 0)
        self.type = "pc"
        self.max_connections = 1
        self.connections = [None] * self.max_connections

        self._gui = dict()
        self._gui_states = dict()
        self.mac = self.get_random_mac()

        self.responses = [None] * self.max_connections
        self.requests = [None] * self.max_connections

    def show_gui(self):
        anchor = {
            "left": "right",
            "right": "right",
            "top": "top",
            "bottom": "bottom"
        }

        first_rect = Rect(10, 5, 150, 30)
        second_rect = Rect(10, 40, 150, 30)
        third_rect = Rect(10, 75, 150, 30)
        last_rect = Rect(10, 110, 150, 30)

        first_rect.right = second_rect.right = third_rect.right = last_rect.right = -10

        self.ui_window = UIWindow(Rect(self.pos, (300, 400)), self.window.ui_manager, "PC " + self.mac)

        self._gui = {
            "message": UITextEntryLine(first_rect, self.window.ui_manager, self.ui_window, anchors=anchor),
            "reciever": UITextEntryLine(second_rect, self.window.ui_manager, self.ui_window, anchors=anchor),
            "send": UIButton(third_rect, "Send", self.window.ui_manager, self.ui_window, anchors=anchor),
            "label1": UILabel(Rect(10, 5, 70, 30), "Message", self.window.ui_manager, self.ui_window),
            "label2": UILabel(Rect(10, 40, 70, 30), "MAC", self.window.ui_manager, self.ui_window),
            "label3": UILabel(Rect(10, 110, 70, 30), "Your MAC", self.window.ui_manager, self.ui_window),
            "last_message": UITextBox("Last message:", Rect(10, 145, 250, 180),
                                      self.window.ui_manager, container=self.ui_window),
            "mac": UITextEntryLine(last_rect, self.window.ui_manager, self.ui_window, anchors=anchor)
        }
        self._gui["mac"]._process_text_entry_key = lambda e: True
        self._gui["mac"].set_text(self.mac)

        if "last_message" not in self._gui_states.keys():
            self._gui_states["last_message"] = "Last message:"

        self.load_gui_state()

    def tick(self):
        if self.requests[0] is not None:
            if self.connections[0] is not None:
                self.connections[0].send(self.requests[0], self)
            else:
                if "last_message" in self._gui.keys():
                    self._gui["last_message"].html_text = "Last message:<br>No connection"
                    self._gui["last_message"].rebuild()
                else:
                    self._gui_states["last_message"] = "Last message:<br>No connection"
        if self.responses[0] is not None:
            print("\nPC " + self.mac, self.responses[0])
            if "last_message" in self._gui.keys():
                self._gui["last_message"].html_text = "Last message:<br>" + str(self.responses[0])
                self._gui["last_message"].rebuild()
            else:
                self._gui_states["last_message"] = "Last message:<br>" + str(self.responses[0])

            if self.responses[0].type == "mac":
                self.connections[0].send(Frame("mac", self.mac, self.responses[0].sender, self.mac), self)
            if self.responses[0].type == "error":
                if self.confirming:
                    if self.wait_cycle < self.max_wait_cycles:
                        self.wait_cycle += 1
                        self.requests[0] = self.confirming_frame
                    else:
                        self.confirming = False
                        self.wait_cycle = 0
                        self.confirming_frame = None

                        if "last_message" in self._gui.keys():
                            self._gui["last_message"].html_text = "Last message:<br>Device not found!"
                            self._gui["last_message"].rebuild()
                        else:
                            self._gui_states["last_message"] = "Last message:<br>Device not found!"
            if self.responses[0].type == "send":
                self.connections[0].send(Frame("received", "Frame recieved", self.responses[0].sender, self.mac), self)
            if self.responses[0].type == "received":
                self.confirming = False
                self.wait_cycle = 0
                self.confirming_frame = None

            self.responses[0] = None

    def handle_event(self, element):
        if element == "send":
            if Object.parse_mac(self._gui["reciever"].get_text()):
                if len(self.connections) > 0:
                    self.requests[0] = Frame("send", self._gui["message"].get_text(),
                                             self._gui["reciever"].get_text(), self.mac)

    def save_gui_state(self):
        self._gui_states.clear()
        self.pos = self.ui_window.get_abs_rect().topleft
        self._gui_states["last_message"] = self._gui["last_message"].html_text
        for el in self._gui:
            if hasattr(self._gui[el], "get_text"):
                self._gui_states[el] = self._gui[el].get_text()

    def load_gui_state(self):
        self._gui["last_message"].html_text = self._gui_states["last_message"]
        self._gui["last_message"].rebuild()
        if len(self._gui_states) < 2:
            return

        self.ui_window.set_position(self.pos)
        for el in self._gui:
            if hasattr(self._gui[el], "get_text"):
                self._gui[el].set_text(self._gui_states[el])
