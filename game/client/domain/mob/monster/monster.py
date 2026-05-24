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

    def change_state(self,new_state,side):
        if side == 0:
            self.animation.direction = "right"
        else :
            self.animation.direction = "left"

        pass

class Laseroide(Monster) :

    def __init__(self, x,y,pos_chunk,cell_size,state):

        super().__init__(x,y,cell_size,size=(8,8),name="Laseroide")

        self.name = "Laseroide"
        self.chunk = pos_chunk
        self.state = state
        self.frame_perso = []
        self.frame = 0
        #self.width ,self.height = self.Img.get_size() #Get la taille de l'img
        self.frame_multiplier = 0

    def change_state(self,new_state,side):
        """Base pour mettre anim"""

        if side == 0:
            self.animation.direction = "right"
        else :
            self.animation.direction = "left"

        key = [key for key,val in STATES.items() if val == new_state]

        if key[0] != self.animation.old_state :
            self.animation.set_state(key[0])

        self.animation.old_state = key[0]

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

    def change_state(self,new_state,side):
        """Base pour mettre anim"""
        if side == 0:
            self.animation.direction = "right"
        else :
            self.animation.direction = "left"

        key = [key for key,val in STATES.items() if val == new_state]

        if key[0]=="attacking" and self.animation.old_state != "attacking":
            self.animation.set_state("attacking")
            self.animation.fct_to_do = self.animation.next_idle

        self.animation.old_state = key[0]

class Defendeur(Monster) :

    def __init__(self, x,y,pos_chunk,cell_size,state):

        super().__init__(x,y,cell_size,size=(10,10),name="Defendeur")

        self.name = "Defendeur"
        self.chunk = pos_chunk
        self.state = state
        self.frame_perso = []
        self.frame = 0
        #self.width ,self.height = self.Img.get_size() #Get la taille de l'img
        self.frame_multiplier = 0

        self.animation.animation["attacking"]["time"] = 0.1
        self.animation.animation["idle"]["time"] = 2/4

    def change_state(self,new_state,side):
        """Base pour mettre anim"""
        if side == 0:
            self.animation.direction = "right"
        else :
            self.animation.direction = "left"

        key = [key for key,val in STATES.items() if val == new_state]

        if key[0] != self.animation.old_state :
            self.animation.set_state(key[0])

        self.animation.old_state = key[0]

class Escargot(Monster) :

    def __init__(self, x,y,pos_chunk,cell_size,state):

        super().__init__(x,y,cell_size,size=(8,8),name="Escargot")

        self.name = "Escargot"
        self.chunk = pos_chunk
        self.state = state
        self.frame_perso = []

        #Inutile ----
        self.frame = 0
        #self.width ,self.height = self.Img.get_size() #Get la taille de l'img
        self.frame_multiplier = 0
        #------

        self.animation.animation["running"]["time"] = 0.3

    def change_state(self,new_state,side):
        """Base pour mettre anim"""
        if side == 0:
            self.animation.direction = "right"
        else :
            self.animation.direction = "left"

        key = [key for key,val in STATES.items() if val == new_state]

        if key[0] != self.animation.old_state :
            self.animation.set_state(key[0])

        self.animation.old_state = key[0]

class Wall(Monster) :

    def __init__(self, x,y,pos_chunk,cell_size,state):

        super().__init__(x,y,cell_size,size=(8,8),name="Wall")

        self.name = "Wall"
        self.chunk = pos_chunk
        self.state = state
        self.frame_perso = []

    def change_state(self,new_state,side):
        """Base pour mettre anim"""
        if side == 0:
            self.animation.direction = "right"
        else :
            self.animation.direction = "left"

        key = [key for key,val in STATES.items() if val == new_state]

        if key[0] != self.animation.old_state :
            self.animation.set_state(key[0])

        self.animation.old_state = key[0]

class WallBig(Monster) :

    def __init__(self, x,y,pos_chunk,cell_size,state):

        super().__init__(x,y,cell_size,size=(8,8),name="WallBig")

        self.name = "WallBig"
        self.chunk = pos_chunk
        self.state = state
        self.frame_perso = []

    def change_state(self,new_state,side):
        """Base pour mettre anim"""
        if side == 0:
            self.animation.direction = "right"
        else :
            self.animation.direction = "left"

        key = [key for key,val in STATES.items() if val == new_state]

        if key[0] != self.animation.old_state :
            self.animation.set_state(key[0])

        self.animation.old_state = key[0]


class DwarfKing(Monster) :
    """Boss : Le Roi Nain. Utilise temporairement la texture du joueur
    (les joueurs sont des nains, le boss leur ressemble)."""

    def __init__(self, x,y,pos_chunk,cell_size,state):

        #name="player" : réutilise la texture du joueur (provisoire), taille ~3.5x le joueur
        super().__init__(x,y,cell_size,size=(28,28),name="player")

        self.name = "DwarfKing"
        self.chunk = pos_chunk
        self.state = state

    def change_state(self,new_state,side):
        """La texture du joueur n'a que idle/running : on y ramène les états du boss."""

        if side == 0:
            self.animation.direction = "right"
        else :
            self.animation.direction = "left"

        anim = {0:"idle", 1:"running", 2:"running", 4:"running", 5:"idle"}.get(new_state,"idle")

        if anim != self.animation.old_state :
            self.animation.set_state(anim)

        self.animation.old_state = anim

class Limace(Monster) :

    def __init__(self, x,y,pos_chunk,cell_size,state):

        super().__init__(x,y,cell_size,size=(8,8),name="Limace")

        self.name = "Limace"
        self.chunk = pos_chunk
        self.state = state
        self.frame_perso = []

        #Inutile ----
        self.frame = 0
        #self.width ,self.height = self.Img.get_size() #Get la taille de l'img
        self.frame_multiplier = 0
        #------

        self.animation.animation["idle"]["time"] = 0.5
        self.animation.animation["attacking"]["time"] = 1
        self.animation.animation["running"]["time"] = 0.2
        self.animation.animation["loading"]["time"] = 1/4

    def change_state(self,new_state,side):
        """Base pour mettre anim"""
        if side == 0:
            self.animation.direction = "right"
        else :
            self.animation.direction = "left"

        key = [key for key,val in STATES.items() if val == new_state]

        if key[0] != self.animation.old_state :
            self.animation.set_state(key[0])

        self.animation.old_state = key[0]


