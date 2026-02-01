from shared.constants import world,size_display
from serv.domain.mob.mob import Mob
from serv.domain.weapon.weapon_manager import WeaponManager

class Player(Mob) :
    '''IL FAUT METTRE EN PLACE LA VITESSE HORIZONTALE ET L'APPLIQUER DANS LES MOUVEMENTS,
    il faut aussi rajouter les dashs (vitesse horizontale temporaire) et les sauts (vitesse verticale négative)'''

    def __init__(self,pos,id,host = False, hp = 100, damage = 25, vitesse_x=1, vitesse_y=1): 

        super().__init__(pos,hp,id,size_display.PLAYER_SIZE_WIDTH,size_display.PLAYER_SIZE_HEIGHT)

        self.hp = hp

        self.damage_taken = damage
        self.is_host = host
        self.vitesse_max = 50*self.base_movement

        self.size_x = 2

        self.weapons = WeaponManager()

        self.next_allowed_shot = 0
        self.time_shot_update = False

    def return_weapon_info(self):
        return self.weapons.return_all_weapon()
    
    def return_weapon_select(self):

        return self.weapons.return_weapon_select()
    
    def update_next_allowed_shot(self,next_allowed_shot):
        self.next_allowed_shot = next_allowed_shot
        self.time_shot_update = True

    def return_next_allowed_shot(self):
        if self.time_shot_update :
            self.time_shot_update=False
            return [self.next_allowed_shot]
        else :
            return []


    def return_delta_vitesse(self,map,dt):

        self.gravity_effect()
        #print(self.pos_x,self.pos_y)

        if self.convert_to_base(self.vitesse_x*dt+self.pos_x)>=self.screen_global_size[0]+self.size_x or self.convert_to_base(self.vitesse_x*dt+self.pos_x)<0:
            self.vitesse_x=0

        if self.convert_to_base(self.vitesse_y*dt+self.pos_y)>=self.screen_global_size[1] or self.convert_to_base(self.vitesse_y*dt+self.pos_y)<0:
            self.vitesse_y=0

        deltax = self.collision_x(map,dt)

        deltay = self.collision_y(map,dt)


        #print(self.pos_x,self.vitesse_x,self.convert_to_base(self.vitesse_x+self.pos_x),self.screen_global_size[0])

        return (deltax,deltay)

    def update_vitesse(self):

        if self.vitesse_x<0:
            self.vitesse_x+=self.acceleration*self.acceleration_x

        elif self.vitesse_x>0:
            self.vitesse_x-=self.acceleration*self.acceleration_x

    def update_pos(self,map,dt):

        delta = self.return_delta_vitesse(map,dt)

        self.update_vitesse()

        self.take_damage(1)

        #print(self.pos_x,self.pos_y)

        return delta
        
    def move_from_key(self,delta,map): 
        '''déplacement en fonction des collisions, peut rajouter un paramètre vitesse plus tard'''

        if delta==0:
            self.move_up(map)

        elif delta==1:
            self.move_down()

        elif delta==2:
            self.move_left()

        elif delta==3:
            self.move_right()
        
        #delta_collision = self.colision(delta, cells_arr, cell_dur, cell_vide, cell_liquid)        
        #self.pos_x += delta_collision[0] 
        #self.pos_y += delta_collision[1] 
        #return delta_collision

    def move_up(self,map):
        #self.pos_y-=1
        if self.touch_ground(map) and self.vitesse_y > -10*self.base_movement:
            self.vitesse_y=-self.acceleration_y

    def move_down(self):
        #self.pos_y+=1
        if self.vitesse_y<self.vitesse_max:
            self.vitesse_y+=self.acceleration*self.acceleration_x

    def move_left(self):
        #self.pos_x-=1
        if self.vitesse_x>-self.vitesse_max:
            self.vitesse_x-=self.acceleration*self.acceleration_x

    def move_right(self):
        #self.pos_x+=1
        if self.vitesse_x<self.vitesse_max:
            self.vitesse_x+=self.acceleration*self.acceleration_x
    
    def take_damage(self, amount):
        self.life -= amount
        if self.life < 10:
            self.life = 10

        self.send_new_life = True
    
    def is_alive(self):
        return self.life > 0