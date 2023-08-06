import pygame
import math
import random



class Ball:
    MAX_VEL = 7
    RADIUS = 7
    GOLD = (255, 215, 0)
    RED = (255, 0, 0)

    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y
        
        angle = self._get_random_angle(-30, 30, [0])
        pos = 1 if random.random() < 0.5 else -1

        self.x_velo = pos * abs(math.cos(angle) * self.MAX_VEL)
        self.y_velo = math.sin(angle) * self.MAX_VEL
        self.border_width = 2

    def _get_random_angle(self, min_angle, max_angle, excluded):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))

        return angle

    def draw(self, my_win):
        pygame.draw.circle(my_win, self.GOLD, (self.x, self.y), self.RADIUS)
        pygame.draw.circle(my_win, self.RED, (self.x,self.y), self.RADIUS)
    def move(self):
        self.x += self.x_velo
        self.y += self.y_velo

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

        angle = self._get_random_angle(-30, 30, [0])
        x_velo = abs(math.cos(angle) * self.MAX_VEL)
        y_velo = math.sin(angle) * self.MAX_VEL

        self.y_velo = y_velo
        self.x_velo *= -1
