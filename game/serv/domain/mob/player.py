from shared.constants import size_display
from serv.domain.mob.mob import Mob
from serv.domain.mob.Upgrade_handler import UpgradeHandler
from serv.domain.weapon.weapon_manager import WeaponManager
from serv.domain.mob.deplacement import smooth_jump,input_handler
from serv.domain.mob.team import Team

class Player(Mob) :
    '''IL FAUT METTRE EN PLACE LA VITESSE HORIZONTALE ET L'APPLIQUER DANS LES MOUVEMENTS,
    il faut aussi rajouter les dashs (vitesse horizontale temporaire)'''

    def __init__(self,pos,id,host = False, hp = 100, damage = 25, vitesse_x=1, vitesse_y=1, money=0): 

        super().__init__(pos,hp,id,size_display.PLAYER_SIZE_WIDTH,size_display.PLAYER_SIZE_HEIGHT,Team.Player)

        self.hp = hp
        self.money = money
        self.send_new_money = False

        self.damage_taken = damage
        self.is_host = host
        self.vitesse_max = 30*self.base_movement
        self.distance_cast_spells = self.half_width
        self.is_looking = 0 #0 = right / 1 = Top / 2 left / 3 bottom

        self.weapons = WeaponManager(self.team)
        self.upgrade_handler = UpgradeHandler()
        self.smooth_jump = smooth_jump.SmoothJump()
        self.input_handler = input_handler.InputHandler()

        self.time_shot_update = False

    def return_weapon_info(self):
        return self.weapons.return_all_weapon()
    
    def return_weapon_select(self):

        return self.weapons.return_weapon_select()
    
    def update_next_allowed_shot(self,id_weapon):
        self.weapon_shot_update=id_weapon

        self.time_shot_update = True

    def return_next_allowed_shot(self):
        if self.time_shot_update :
            self.time_shot_update=False
            time = self.weapons.lWeapons[self.weapon_shot_update].return_info_next_time_can_shot()
            return [time,self.weapon_shot_update]
        else :
            return []

    def return_delta_vitesse(self,map,dt):

        old_pos_x = self.pos_x
        old_pos_y = self.pos_y

        self.gravity_effect()
        
        self.upgrade_handler.trigger_event_on_player(self.weapons.id_event_player_do,self,dt,map)

        self.collision_x(map,dt,self.vitesse_x)

        self.collision_y(map,dt,self.vitesse_y)

        delta_x = self.pos_x-old_pos_x
        delta_y = self.pos_y-old_pos_y

        return (delta_x,delta_y)

    def update_vitesse(self):

        s = self.return_signe(self.vitesse_x)

        if self.vitesse_x*s<self.acceleration:
            self.vitesse_x = 0
        else :
            #self.vitesse_x-=self.acceleration_x*s#self.acceleration_x
            self.vitesse_x=self.vitesse_x*0.8

    def update_pos(self,map,dt):

        delta = self.return_delta_vitesse(map,dt)

        self.update_vitesse()

        self.smooth_jump.trigger(self.touch_ground(map),self.vitesse_y)

        self.handle_input(map)

        return delta
    
    def handle_input(self,map):

        val = self.input_handler.trigger()

        for input in (val):

            self.move_from_input(input[0],input[1],map)
                

    def move_from_input(self,idx,dt,map):

        if idx==0:
            self.move_up(map)

        elif idx==1:
            self.move_down(dt)

        elif idx==2:
            self.move_left(dt)

        elif idx==3:
            self.move_right(dt)
        
    def move_from_key(self,delta,map,dt_receive): 
        '''déplacement en fonction des collisions, peut rajouter un paramètre vitesse plus tard'''

        dt = dt_receive/1000

        # Check for ladder interaction
        if self.is_on_ladder(map):
            if delta == 0: # UP
                self.climb(map, -1, dt)
                return
            elif delta == 1: # DOWN
                self.climb(map, 1, dt)
                return
            
            # If moving side-ways on ladder, maybe fall off?
            # For now let's keep is_climbing true unless we move off
            
        else:
            self.is_climbing = False

        #0 : up/1 : down/ 2 : left/ 3 : right

        self.input_handler.update_value(delta,dt)

        #if delta==0:
        #    self.move_up(map)
#
        #elif delta==1:
        #    self.move_down(dt)
#
        #elif delta==2:
        #    self.move_left(dt)
#
        #elif delta==3:
        #    self.move_right(dt)

    def move_up(self,map):
        #self.pos_y-=1
        self.is_looking=1
        if self.can_jump():

        #if self.touch_ground(map) and self.vitesse_y > -10*self.base_movement:
            self.vitesse_y=-self.acceleration_y

    def can_jump(self):
        
        if self.smooth_jump.can_jump():
            return True



    def move_down(self,dt):
        #self.pos_y+=1
        self.is_looking=3
        if self.vitesse_y<self.vitesse_max:
            self.vitesse_y+=self.acceleration_y*dt
            
    def move_left(self,dt):
        self.is_looking = 2
        s=self.return_signe(self.vitesse_x)

        if self.vitesse_x>-self.vitesse_max:
            self.vitesse_x-=self.acceleration*self.acceleration_x*dt
            self.vitesse_x*=(1-0.2*s)

        if self.vitesse_x<-self.vitesse_max:
            self.vitesse_x = -self.vitesse_max

    def move_right(self,dt):
        self.is_looking = 0
        s=self.return_signe(self.vitesse_x)

        if self.vitesse_x<self.vitesse_max:
            self.vitesse_x+=self.acceleration*self.acceleration_x*dt
            self.vitesse_x*=(1+0.2*s)

        if self.vitesse_x>self.vitesse_max:
            self.vitesse_x = self.vitesse_max
    
    def is_alive(self):
        return self.life > 0
    
    def update_money(self, amount):

        self.money+= amount

        self.send_new_money = True
    
    def send_money(self):
        self.send_new_money = False
        return self.money


    def switch_spell(self,spell_1_weapon,spell_1_idx,spell_2_weapon,spell_2_idx):

        spell_switch = self.weapons.lWeapons[spell_1_weapon].spells_on_shot[spell_1_idx]
        self.weapons.lWeapons[spell_1_weapon].spells_on_shot[spell_1_idx] = self.weapons.lWeapons[spell_2_weapon].spells_on_shot[spell_2_idx]
        self.weapons.lWeapons[spell_2_weapon].spells_on_shot[spell_2_idx] = spell_switch

    def shot(self,id_weapon):

        angle = self.is_looking

        pos = self.return_pos_for_shot(angle)

        return self.weapons.create_shot(id_weapon,pos,angle)
    
    def return_pos_for_shot(self,angle):
        pos = self.return_pos()

        if angle==2: #x
            pos[0]-=self.distance_cast_spells
        elif angle==0:
            pos[0]+=self.distance_cast_spells

        elif angle==1:#y
            pos[1]-=self.distance_cast_spells
        elif angle==3:
            pos[1]+=self.distance_cast_spells

        return pos
