import pygame


class Paddle:
    VELOCITY = 6
    WIDTH = 25
    HEIGHT = 110
    RED = (255, 0, 0)
    GOLD = (255, 215, 0)

    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y

    def draw(self, my_win):
        pygame.draw.rect(my_win, self.GOLD, (self.x, self.y, self.WIDTH, self.HEIGHT),0)
        for _ in range(4):
            pygame.draw.rect(my_win, self.RED, (self.x - _, self.y - _, self.WIDTH + 5, self.HEIGHT + 5), 1)

    def move(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
