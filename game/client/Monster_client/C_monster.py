import pygame

class Skeleton :

    def __init__(self, x,y,pos_chunk):
        self.name = "Skeleton"
        self.pos_x = x
        self.pos_y = y
        self.chunk = pos_chunk
        self.Img = pygame.image.load("assets/playerImg.png").convert_alpha()

        self.width ,self.height = self.Img.get_size() #Get la taille de l'img