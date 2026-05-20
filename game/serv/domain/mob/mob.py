from shared.constants import world
from serv.domain.mob.deplacement.moves import Movable
from serv.domain.mob.deplacement import smooth_jump
from serv.domain.mob.team import Team

class Mob(Movable):

    def __init__(self,pos,hp = 100,id=None,width=10,height=10,team = Team.Mob,len_dead = 5,acceleration = 1):
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        
        self.smooth_jump = smooth_jump.SmoothJump()

        self.len_dead = len_dead
        self.start_dead = 0

        self.screen_global_size = world.BG_SIZE_SERVER

        self.base_movement = world.RATIO #C'est le mouv de base = si ajoute 100, se deplace de 1 carre plus vite

        self.acceleration = acceleration*self.base_movement
        self.gravity_power = 1
        self.vitesse_down_base = self.acceleration*self.gravity_power
        self.acceleration_x = 2 * self.acceleration
        self.acceleration_y = 10 * self.acceleration
        self.jump_strenght = 150 * self.acceleration
        self.frottement_power = 0.75
        self.vitesse_max = 100*self.base_movement
        self.vitesse_x = 0
        self.vitesse_y = 0

        self.in_dash = False
        
        self.width = (width)*self.base_movement
        self.half_width = self.width//2
        self.height = height*self.base_movement
        self.half_height = self.height//2

        self.life = hp
        self.max_life = hp
        self.send_new_life = True #Pour initialiser
        self.id = id
        self.team = team
        self.dead = False

    def send_life(self):
        self.send_new_life = False
        return self.life,self.max_life,self.id

    def return_pos(self):
        return [self.pos_x,self.pos_y]

    def full_heal(self):

        if self.life != self.max_life :
            self.life = self.max_life
            self.send_new_life = True

    def add_life(self,amount):

        self.max_life+= amount
        self.send_new_life = True

    #-----------------Choses que le joueur utilise ! donc fonctionne-------------------#
    
    def jump(self,map,force_jump = False):

        if force_jump or self.can_jump():
        #if self.touch_ground(map) and self.vitesse_y > -10*self.base_movement:
            self.vitesse_y=-self.jump_strenght

            return True
        return False

            
    def move_left(self,dt):
        self.is_looking = 2
        s=self.return_signe(self.vitesse_x)

        if self.vitesse_x>-self.vitesse_max:
            self.vitesse_x-=self.acceleration*self.acceleration_x*dt
            self.vitesse_x*=(1-0.1*s)

        if self.vitesse_x<-self.vitesse_max:
            self.vitesse_x = -self.vitesse_max

    def move_right(self,dt):
        self.is_looking = 0
        s=self.return_signe(self.vitesse_x)

        if self.vitesse_x<self.vitesse_max:
            self.vitesse_x+=self.acceleration*self.acceleration_x*dt
            self.vitesse_x*=(1+0.1*s)

        if self.vitesse_x>self.vitesse_max:
            self.vitesse_x = self.vitesse_max

    def move_up(self,dt,map):
        #self.pos_y-=1
        self.is_looking=1

        if self.can_climb(map):
            #self.is_climbing = True
            self.vitesse_y = -self.acceleration_y*dt*self.acceleration

        #else :
        #    self.is_climbing = False

    def move_down(self,dt):
        #self.pos_y+=1
        self.is_looking=3
        if self.vitesse_y<self.vitesse_max:
            self.vitesse_y+=self.acceleration_y*dt

    def return_delta_vitesse(self,map,dt):

        old_pos_x = self.pos_x
        old_pos_y = self.pos_y

        self.gravity_effect(dt)

        self.collision_x(map,dt,self.vitesse_x)

        self.collision_y(map,dt,self.vitesse_y)

        delta_x = self.pos_x-old_pos_x
        delta_y = self.pos_y-old_pos_y

        return (delta_x,delta_y)
    
    def update_vitesse(self,dt):

        s = self.return_signe(self.vitesse_x)

        if self.vitesse_x*s<self.acceleration:
            self.vitesse_x = 0
        else :

            self.vitesse_x = self.vitesse_x*(self.frottement_power**(dt*60))

    def move_all(self,map,dt,collision_handler):

        self.smooth_jump.trigger(self.touch_ground(map),self.vitesse_y)

        delta = self.return_delta_vitesse(map,dt)

        self.update_vitesse(dt)

        return delta

    def can_jump(self):
        
        if self.smooth_jump.can_jump():
            return True