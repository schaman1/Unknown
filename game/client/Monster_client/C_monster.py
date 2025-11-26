import pygame

class Skeleton :

    def __init__(self, x,y):
        self.name = "Skeleton"
        self.pos_x = x
        self.pos_y = y
        self.Img = pygame.image.load("assets/playerImg.png").convert_alpha()