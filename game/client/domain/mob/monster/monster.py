import pygame
from client.config import assets
from client.domain.mob.mob import Mob
from utils.resource_path import resource_path
from client.domain.mob.monster.states import STATES
import os

class Monster(Mob):

    def __init__(self,x,y,cell_size,size,name):

        super().__init__(x,y,cell_size,size=size,name=name)

    def blit(self,screen,x,y,dt):

        self.update_interpolate_pos()
        self.animation.draw(dt,self.calculate_pos_blit(x,y),screen)

        return
    
    def move(self,delta):

        dx = delta[0]*self.cell_size//self.base_movement-self.pos_x

        if dx<0:
            self.animation.direction = "left"
        elif dx>0:
            self.animation.direction = "right"

        new_pos = self.convert_from_base(delta[0]*self.cell_size),self.convert_from_base(delta[1]*self.cell_size)
        self.move_mob(new_pos)

    def kill(self,duree):

        self.animation.set_to_death(duree,"death")


class Skeleton(Monster) :

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

    def update_frame(self):
        self.frame_multiplier +=1
        if self.frame_multiplier >= 10 :
            self.frame +=1
            self.frame_multiplier = 0

    def change_state(self,new_state):

        pass

class Laseroide(Monster) :

    def __init__(self, x,y,pos_chunk,cell_size,state):

        super().__init__(x,y,cell_size,size=(8,6),name="Laseroide")

        self.name = "Laseroide"
        self.chunk = pos_chunk
        self.state = state
        self.frame_perso = []
        self.frame = 0
        #self.width ,self.height = self.Img.get_size() #Get la taille de l'img
        self.frame_multiplier = 0

    def change_state(self,new_state):

        key = [key for key,val in STATES.items() if val == new_state]

        if key[0]=="loading" and self.animation.state != "loading":
            self.animation.set_state("loading")
            self.animation.fct_to_do = self.animation.next_idle

        elif key[0] != "loading" :

            self.animation.state = "idle"

class Foulli(Monster) :

    def __init__(self, x,y,pos_chunk,cell_size,state):

        super().__init__(x,y,cell_size,size=(8,6),name="Foulli")

        self.name = "Foulli"
        self.chunk = pos_chunk
        self.state = state
        self.frame_perso = []
        self.frame = 0
        #self.width ,self.height = self.Img.get_size() #Get la taille de l'img
        self.frame_multiplier = 0

        self.old_state = None

    def change_state(self,new_state):
        """Base pour mettre anim"""

        key = [key for key,val in STATES.items() if val == new_state]

        if key[0]=="attacking" and self.old_state != "attacking":
            self.animation.set_state("attacking")
            self.animation.fct_to_do = self.animation.next_idle

        self.old_state = key[0]

class Defendeur(Monster) :

    def __init__(self, x,y,pos_chunk,cell_size,state):

        super().__init__(x,y,cell_size,size=(8,8),name="Defendeur")

        self.name = "Defendeur"
        self.chunk = pos_chunk
        self.state = state
        self.frame_perso = []
        self.frame = 0
        #self.width ,self.height = self.Img.get_size() #Get la taille de l'img
        self.frame_multiplier = 0

        self.old_state = None

    def change_state(self,new_state):
        """Base pour mettre anim"""

        key = [key for key,val in STATES.items() if val == new_state]

        if key[0] != self.old_state :
            self.animation.set_state(key[0])

        self.old_state = key[0]