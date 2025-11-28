from serv.in_game.C_mobs import mobs
import pygame

class Skeleton(mobs):
    def __init__(self, x,y, id):
        self.name = "Skeleton"
        self.id = id
        self.pos_x = x
        self.pos_y = y
        
    def move(self):
        self.pos_x -= 1  # Exemple simple : le squelette se déplace vers la droite
        self.pos_y+=1
        pass