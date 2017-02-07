"""Menu option class.

based on https://gist.github.com/ohsqueezy/2802185 """

import pygame


class MenuOption:
    hovered = False

    def __init__(self, text, pos, window):
        self.window = window

        self.font = pygame.font.Font(None, 40)
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_rend()
        self.window.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = self.font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return 255, 255, 255
        else:
            return 100, 100, 100

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos
