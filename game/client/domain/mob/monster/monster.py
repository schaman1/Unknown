import pygame
from client.config import assets
from client.domain.mob.mob import Mob
from utils.resource_path import resource_path
import os

class Skeleton(Mob) :

    def __init__(self, x,y,pos_chunk,cell_size,state):

        super().__init__(x,y,cell_size,size=(10,10),name="Skeleton")

        self.name = "Skeleton"
        self.chunk = pos_chunk
        self.state = state
        self.frame_perso = []
        self.frame = 0
        #self.width ,self.height = self.Img.get_size() #Get la taille de l'img
        self.frame_multiplier = 0

        #self.init_Img(cell_size)


    def kill(self,duree):

        self.animation.set_to_death(duree,"death")


    def update_frame(self):
        self.frame_multiplier +=1
        if self.frame_multiplier >= 10 :
            self.frame +=1
            self.frame_multiplier = 0

    def blit(self,screen,x,y,dt):

        self.update_interpolate_pos()
        self.animation.draw(dt,self.calculate_pos_blit(x,y),screen)

        return

    def move(self,delta):
        new_pos = self.convert_from_base(delta[0]*self.cell_size),self.convert_from_base(delta[1]*self.cell_size)
        self.move_mob(new_pos)

class Laseroide(Mob) :

    def __init__(self, x,y,pos_chunk,cell_size,state):

        super().__init__(x,y,cell_size,size=(8,6),name="Laseroide")

        self.name = "Laseroide"
        self.chunk = pos_chunk
        self.state = state
        self.frame_perso = []
        self.frame = 0
        #self.width ,self.height = self.Img.get_size() #Get la taille de l'img
        self.frame_multiplier = 0

        #self.init_Img(cell_size)

    def kill(self,duree):

        self.animation.set_to_death(duree,"death")

    def update_frame(self):
        self.frame_multiplier +=1
        if self.frame_multiplier >= 10 :
            self.frame +=1
            self.frame_multiplier = 0

    def blit(self,screen,x,y,dt):

        self.update_interpolate_pos()
        self.animation.draw(dt,self.calculate_pos_blit(x,y),screen)

        return
    
    def move(self,delta):
        new_pos = self.convert_from_base(delta[0]*self.cell_size),self.convert_from_base(delta[1]*self.cell_size)
        self.move_mob(new_pos)