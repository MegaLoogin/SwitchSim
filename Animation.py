class Animation:
    def __init__(self, size, image, pos, start_tick, game):
        self.size = size
        self.image = image
        self.pos = pos
        self.start_tick = start_tick
        self.game = game

    def get_pos(self, delta):
        diff = delta - self.start_tick
        if diff < 1000 / self.game.tps:
            ratio = diff * self.game.tps / 1000
            return self.pos[0][0] + (self.pos[1][0] - self.pos[0][0]) * ratio, self.pos[0][1] + (self.pos[1][1] - self.pos[0][1]) * ratio
        else:
            for i, an in enumerate(self.game.anims):
                if an == self:
                    self.game.anims.pop(i)
                    return None
