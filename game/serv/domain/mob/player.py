from serv.config import collisions
from serv.domain.mob.mob import Mob
from serv.domain.mob.Upgrade_handler import UpgradeHandler
from serv.domain.weapon.weapon_manager import WeaponManager
from serv.domain.mob.deplacement import input_handler
from serv.domain.mob.team import Team
from serv.config import Default_values
from shared.constants import world
import time

class Player(Mob) :
    '''IL FAUT METTRE EN PLACE LA VITESSE HORIZONTALE ET L'APPLIQUER DANS LES MOUVEMENTS,
    il faut aussi rajouter les dashs (vitesse horizontale temporaire)'''

    def __init__(self,pos,id,host = False,damage = 25): 

        super().__init__(pos=pos,hp=Default_values.PLAYER_LIFE,id=id,width=collisions.PLAYER_COLLISION_X,height=collisions.PLAYER_COLLISION_Y,team=Team.Player,len_dead = world.LEN_DEATH_PLAYER)

        self.money = Default_values.Player_money_start
        self.send_new_money = True #Pour initialiser

        self.damage_taken = damage
        self.is_dead = False
        self.has_respawn = True

        self.is_host = host
        self.distance_cast_spells = self.half_width
        self.is_looking = 0 #0 = droite / 1 = haut / 2 = gauche / 3 = bas

        self.weapons = WeaponManager(self.team,self)
        self.upgrade_handler = UpgradeHandler()
        self.input_handler = input_handler.InputHandler()

        self.time_shot_update = False
        self.respawn_at = [self.pos_x,self.pos_y]
        self.time_respawn = 0

        self.last_time_touch_lave = time.perf_counter()
        self.len_lave_touch = 0.2

        self.fct_to_do = self.check_if_can_leave_intro #Here to check if can leave after intro

    def set_finish_intro(self):
        self.fct_to_do = self.empty_fct
    
    def empty_fct(self):
        return False

    def check_if_can_leave_intro(self):

        if self.pos_x <= world.POS_TOO_LEFT*self.base_movement :
            return True
        return False

    def take_damage(self, amount):
        """Retourne True/False selon si le joueur est mort ou non"""

        if amount!=0 and self.is_dead == False:

            self.life -= amount
            self.send_new_life = True

            if self.life <= 0 :
                self.life = 0
                self.die()

                return True
            
        return False

    def die(self):
        self.is_dead = True
        self.has_respawn = False
        self.start_dead = time.perf_counter()+ self.len_dead
        self.update_money(-50)
        self.input_handler.stop_mov()

    def respawn(self):

        self.pos_x = self.respawn_at[0]
        self.pos_y = self.respawn_at[1]
        self.has_respawn = True

    def can_move_after_death(self):
        self.is_dead = False
        self.full_heal()

    def check_respawn(self):

        if not self.has_respawn and time.perf_counter()>=self.start_dead-0.2*4:
            self.respawn()

        if self.is_dead and time.perf_counter()>=self.start_dead :
            self.can_move_after_death()

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

    def update_pos(self,map,dt,collision_handler):

        print("pos :",self.pos_x,self.pos_y-self.half_height)

        self.check_respawn()

        if not self.is_dead : #Permet que quand est mort, trigger plus les input du joueur

            self.handle_input(map,dt)

        self.upgrade_handler.trigger_event_on_player(self,dt,map)

        self.move_all(map,dt,collision_handler)

        if self.last_time_touch_lave + self.len_lave_touch < time.perf_counter():
            if collision_handler.check_if_touch_damage_obj(map,dt,self) :
                self.last_time_touch_lave = time.perf_counter()
    
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

        self.input_handler.update_value(key)
        
        if key == 1 :
            self.is_climbing = False

    def stop_from_key(self,key,map):

        self.input_handler.set_false(key)

        if key == 1 :
            self.is_climbing = True

    def is_alive(self):
        return self.life > 0
    
    def update_money(self, amount):

        old_money = self.money
        self.money+= amount

        if self.money<0:
            self.money = 0

        if self.money-old_money!=0 :

            self.send_new_money = True
    
    def send_money(self):
        self.send_new_money = False
        return self.money

    def switch_spell(self,spell_1_weapon,spell_1_idx,spell_2_weapon,spell_2_idx):

        spell_switch = self.weapons.lWeapons[spell_1_weapon].spells_on_shot[spell_1_idx]
        self.weapons.lWeapons[spell_1_weapon].spells_on_shot[spell_1_idx] = self.weapons.lWeapons[spell_2_weapon].spells_on_shot[spell_2_idx]
        self.weapons.lWeapons[spell_2_weapon].spells_on_shot[spell_2_idx] = spell_switch

    def shot(self,id_weapon):
        """Tire, mais ne tire pas si le joueur est mort"""

        if self.is_dead :
            return

        angle = self.is_looking

        pos = self.return_pos_for_shot(angle)

        projectiles,player_event,monsters_create = self.weapons.create_shot(id_weapon,pos,angle)

        if player_event!=None :

            self.upgrade_handler.add_event(player_event,self)

        return projectiles,monsters_create
    
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

    def heal_respawn(self,element):

        self.full_heal()

        self.set_respawn_point(element)

    def set_respawn_point(self,element):

        self.respawn_at = [element.pos_x,element.pos_y]

    def upgrade_size_weapon(self,nbr):

        for _ in range(nbr) :
            infos = self.weapons.add_slot()

        return infos
    
    def unlock_double_jump(self):
        self.smooth_jump.double_jump = True #Now can double jump !

    def reduce_time(self):
        return self.weapons.reduce_time()