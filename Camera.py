import pygame


class Camera:
    def __init__(self, game, pos, zoom):
        size = game.window.screen.get_size()
        self.game = game
        self.zoom = zoom
        self.pos = pos

        self.zoom_pos = size[0] / 2, size[1] / 2

    def update_camera(self):
        size = self.game.window.screen.get_size()
        self.zoom_pos = size[0] / 2, size[1] / 2

    def move(self, shift):
        self.pos = self.pos[0] - shift[0] / self.zoom, self.pos[1] - shift[1] / self.zoom

    def get_pos_from_screen(self, point):
        return (point[0] - self.zoom_pos[0]) / self.zoom + self.pos[0], (point[1] - self.zoom_pos[1]) / self.zoom + self.pos[1]

    def draw(self):
        win_size = self.game.window.screen.get_size()

        viewport = pygame.Rect((-win_size[0] / 2 / self.zoom + self.pos[0], -win_size[1] / 2 / self.zoom + self.pos[1]),
                               (win_size[0] / self.zoom, win_size[1] / self.zoom))

        for an in self.game.anims:
            pos = an.get_pos(pygame.time.get_ticks())
            if pos is not None:
                anim_rect = pygame.Rect(pos, an.size)
                if viewport.colliderect(anim_rect):
                    x = ((anim_rect.x - self.pos[0]) * self.zoom) + self.zoom_pos[0]
                    y = ((anim_rect.y - self.pos[1]) * self.zoom) + self.zoom_pos[1]

                    screen_obj_rect = pygame.Rect((x, y), (anim_rect.w * self.zoom, anim_rect.h * self.zoom))
                    scaled_image = pygame.transform.scale(an.image,
                                                          (int(anim_rect.w * self.zoom), int(anim_rect.h * self.zoom)))

                    self.game.window.screen.blit(scaled_image, screen_obj_rect)

        for con in self.game.connections:
            if con is not None:
                line = con.get_line()
                x1 = ((line[0][0] - self.pos[0]) * self.zoom) + self.zoom_pos[0]
                y1 = ((line[0][1] - self.pos[1]) * self.zoom) + self.zoom_pos[1]
                x2 = ((line[1][0] - self.pos[0]) * self.zoom) + self.zoom_pos[0]
                y2 = ((line[1][1] - self.pos[1]) * self.zoom) + self.zoom_pos[1]
                pygame.draw.line(self.game.window.screen, (255, 255, 255), (x1, y1), (x2, y2))

        for obj in self.game.objects:
            if viewport.colliderect(obj.rect):
                x = ((obj.rect.x - self.pos[0]) * self.zoom) + self.zoom_pos[0]
                y = ((obj.rect.y - self.pos[1]) * self.zoom) + self.zoom_pos[1]

                screen_obj_rect = pygame.Rect((x, y), (obj.rect.w * self.zoom, obj.rect.h * self.zoom))
                scaled_image = pygame.transform.scale(obj.image, (int(obj.rect.w * self.zoom), int(obj.rect.h * self.zoom)))
                if obj.selected:
                    pygame.draw.rect(self.game.window.screen, (255, 255, 255), screen_obj_rect, 2)
                self.game.window.screen.blit(scaled_image, screen_obj_rect)
