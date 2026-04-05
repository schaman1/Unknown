from serv.config import collisions
from serv.domain.mob.mob import Mob
from serv.domain.mob.Upgrade_handler import UpgradeHandler
from serv.domain.weapon.weapon_manager import WeaponManager
from serv.domain.mob.deplacement import smooth_jump,input_handler
from serv.domain.mob.team import Team
from serv.config.Default_values import Player_money_start

class Player(Mob) :
    '''IL FAUT METTRE EN PLACE LA VITESSE HORIZONTALE ET L'APPLIQUER DANS LES MOUVEMENTS,
    il faut aussi rajouter les dashs (vitesse horizontale temporaire)'''

    def __init__(self,pos,id,host = False, hp = 100, damage = 25, money=Player_money_start): 

        super().__init__(pos,hp,id,collisions.PLAYER_COLLISION_X,collisions.PLAYER_COLLISION_Y,Team.Player)

        self.hp = hp
        self.money = money
        self.send_new_money = True #Pour initialiser

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

    def can_pick_spell(self):

        return self.weapons.bag_not_full()

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
            #if self.smooth_jump.is_falling :
                #self.vitesse_x=self.vitesse_x*0.99 #Car en l'air peut changer de direction plus difficilement
            if not self.smooth_jump.is_falling :
                self.vitesse_x=self.vitesse_x*0.8

    def update_pos(self,map,dt):

        self.handle_input(map,dt)

        self.smooth_jump.trigger(self.touch_ground(map),self.vitesse_y)

        delta = self.return_delta_vitesse(map,dt)

        self.update_vitesse()

        return delta
    
    def handle_input(self,map,dt):

        val = self.input_handler.trigger()

        for input in (val):

            self.move_from_input(input,dt,map)
                

    def move_from_input(self,idx,dt,map):

        if idx==0:
            self.move_up(dt,map)

        elif idx==1:
            self.move_down(dt)

        elif idx==2:
            self.move_left(dt)

        elif idx==3:
            self.move_right(dt)

        elif idx == 7:
            self.jump(map)
        
    def move_from_key(self,key,map): 
        '''déplacement en fonction des collisions, peut rajouter un paramètre vitesse plus tard'''

        # Check for ladder interaction
        #if self.can_climb(map):
        #    if delta == 0: # UP
        #        self.climb(map, -1, 1)
        #        return
        #    elif delta == 1: # DOWN
        #        self.climb(map, 1, 1)
        #        return
        #    
        #    # If moving side-ways on ladder, maybe fall off?
        #    # For now let's keep is_climbing true unless we move off
        #    
        #else:
        #    self.is_climbing = False

        #0 : up/1 : down/ 2 : left/ 3 : right

        self.input_handler.update_value(key)
        
        if key == 1 :
            self.is_climbing = False

    def stop_from_key(self,key,map):

        self.input_handler.set_false(key)

        if key == 1 :
            self.is_climbing = True

    def jump(self,map):

        if self.can_jump():
        #if self.touch_ground(map) and self.vitesse_y > -10*self.base_movement:
            self.vitesse_y=-self.jump_strenght

    def can_jump(self):
        
        if self.smooth_jump.can_jump():
            return True

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

        if amount!=0 :

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
    
    def remove_spell(self,id_weapon,id_spell):

        spell_id = self.weapons.lWeapons[id_weapon].del_spell(id_spell)

        return spell_id
