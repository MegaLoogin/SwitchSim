import pygame
from Window import *

size = width, height = 1200, 700  # 800, 600


def main():
    pygame.init()

    window = Window(size, "Cursa4")
    window.run_cycle()


if __name__ == '__main__':
    main()


