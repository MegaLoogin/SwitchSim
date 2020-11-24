import pygame
import pygame_gui
from Game import *


class Window:
    def __init__(self, size, caption):
        self.screen = pygame.display.set_mode(size)
        self.size = size
        pygame.display.set_caption(caption)
        self.running = True
        self.ui_manager = pygame_gui.UIManager(size)

        self.fullscreen = False

        self.game = Game(self, (0, 0), 0.5)

        keys = [*self.game.types]
        keys.insert(0, "None")
        keys.append("Connect")

        anchors = {
                "left": "left",
                "right": "right",
                "top": "bottom",
                "bottom": "bottom"
            }
        tps_rect = pygame.Rect(0, 0, 50, 40)
        tps_rect.bottom = 0
        tps_button = pygame.Rect(50, 0, 70, 30)
        tps_button.bottom = -10
        self.gui = {
            "selector": pygame_gui.elements.UIDropDownMenu(keys, "None", pygame.Rect((0, 0, 150, 30)), self.ui_manager),
            "tps": pygame_gui.elements.UITextEntryLine(tps_rect, self.ui_manager, anchors=anchors),
            "set_tps": pygame_gui.elements.UIButton(tps_button, "Set TPS", self.ui_manager, anchors=anchors),

        }

        self.gui["tps"].text = str(self.game.tps)

    def get_collide(self, pos):
        if self.gui["selector"].relative_rect.collidepoint(pos):
            return True
        for el in self.ui_manager.get_window_stack().get_stack():
            if el._window_root_container.rect.collidepoint(pos):
                return True
        return False

    def procces_events(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == "ui_button_pressed":
                    if event.ui_element == self.gui["set_tps"]:
                        try:
                            value = float(self.gui["tps"].get_text())
                            self.game.tps = value
                        except ValueError:
                            self.gui["tps"].set_text(str(self.game.tps))
                    for el in self.game.objects:
                        for gui_el in el._gui:
                            if el._gui[gui_el] == event.ui_element:
                                el.handle_event(gui_el)
                if event.user_type == pygame_gui.UI_WINDOW_CLOSE:
                    for el in self.game.objects:
                        if el.ui_window == event.ui_element:
                            el.save_gui_state()
                if event.user_type == "ui_drop_down_menu_changed":
                    if event.ui_element == self.gui['selector']:
                        self.game.selected_object = self.gui['selector'].selected_option
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    if self.game.buffer_device is not None:
                        self.game.buffer_device.selected = False
                        self.game.buffer_device = None
                if event.key == pygame.K_DELETE:
                    for i, obj in enumerate(self.game.objects):
                        if obj == self.game.buffer_device:
                            self.game.buffer_device.selected = False
                            self.game.buffer_device = None
                            self.game.objects[i].remove_connections()
                            self.game.objects.pop(i)
                '''if event.key == pygame.K_F11:
                    self.fullscreen = not self.fullscreen
                    pygame.display.toggle_fullscreen()
                    if self.fullscreen:
                        self.screen = pygame.display.set_mode((0, 0))
                    else:
                        self.screen = pygame.display.set_mode(self.size)
                    self.game.camera.update_camera()
                    print(self.screen.get_size())
                    self.ui_manager.set_window_resolution(self.screen.get_size())
                    self.ui_manager.clear_and_reset()'''
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not self.get_collide(event.pos):
                        obj = self.game.get_object(self.game.camera.get_pos_from_screen(event.pos))
                        if obj:
                            if self.game.selected_object == "Connect":
                                if self.game.buffer_device is None:
                                    obj.selected = True
                                    self.game.buffer_device = obj
                                else:
                                    if not self.game.buffer_device.type == obj.type:
                                        f_port = self.game.buffer_device.get_free_port()
                                        s_port = obj.get_free_port()
                                        if f_port > -1 and s_port > -1:
                                            self.game.make_connection(self.game.buffer_device, obj, (f_port, s_port))
                                            self.game.buffer_device.selected = False
                                            self.game.buffer_device = None
                            elif not self.game.is_selected():
                                if obj.ui_window is not None:
                                    is_win = True
                                    for win in obj.ui_window.window_stack.stack:
                                        if win == obj.ui_window:
                                            is_win = False
                                            break
                                    if is_win:
                                        obj.show_gui()
                                else:
                                    obj.show_gui()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.game.is_selected():
                    if not self.gui["selector"].current_state == self.gui["selector"].menu_states["expanded"]:
                        if not self.get_collide(event.pos):
                            self.game.place_object(self.game.camera.get_pos_from_screen(event.pos))
            if event.type == pygame.MOUSEWHEEL:
                if not self.get_collide(pygame.mouse.get_pos()):
                    self.game.camera.zoom += event.y * (self.game.camera.zoom / 10)
                    self.game.camera.zoom = max(min(self.game.camera.zoom, 7), 0.5)
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.MOUSEMOTION:
                if event.buttons[2]:
                    if not self.get_collide(event.pos):
                        self.game.camera.move(event.rel)

            self.ui_manager.process_events(event)

    def run_cycle(self):
        clock = pygame.time.Clock()
        last_tick = 0

        while self.running:
            tps_ticks = 1000 / self.game.tps
            now_tick = pygame.time.get_ticks()
            if last_tick + tps_ticks < now_tick:
                last_tick = pygame.time.get_ticks()
                self.game.process_tick()
                # print("----------------TICK------------------")
            self.procces_events()
            # print("draw")
            self.ui_manager.update(clock.tick(60) / 1000.0)
            self.draw_scene()

    def draw_scene(self):
        self.screen.fill((0, 0, 0))

        self.game.camera.draw()
        self.ui_manager.draw_ui(self.screen)

        pygame.display.update()
