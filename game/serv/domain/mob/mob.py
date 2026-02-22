from shared.constants import world
from serv.domain.mob.deplacement.moves import Movable
from serv.domain.mob.team import Team

class Mob(Movable):

    def __init__(self,pos,hp = 100,id=None,width=10,height=10,team = Team.Mob):
        self.pos_x = pos[0]
        self.pos_y = pos[1]

        self.screen_global_size = world.BG_SIZE_SERVER

        self.base_movement = world.RATIO #C'est le mouv de base = si ajoute 100, se deplace de 1 carre plus vite

        self.acceleration = self.base_movement
        self.gravity_power = 1
        self.vitesse_down_base = self.acceleration*self.gravity_power
        self.acceleration_x = 2 * self.acceleration
        self.acceleration_y = 150 * self.acceleration
        self.vitesse_x = 0
        self.vitesse_y = 0
        
        self.width = (width)*self.base_movement
        self.half_width = self.width//2
        self.height = height*self.base_movement
        self.half_height = self.height//2

        self.life = hp
        self.max_life = hp
        self.send_new_life = False
        self.id = id
        self.team = team

    def send_life(self):
        self.send_new_life = False
        return self.life
        
    def return_pos(self):
        return [self.pos_x,self.pos_y]
    
    def take_damage(self, amount):
        self.life -= amount
        if self.life < 10:
            self.life = 10

        self.send_new_life = True