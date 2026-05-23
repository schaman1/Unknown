from shared.constants.world import NBRWEAPONSTOCK
from client.domain.weapon.weapon import Weapon
from client.ui.complete_info import CompleteInfo

#from client.config import size_display as size
import time

class WeaponManager:

    def __init__(self,screen_size,cell_size):

        self.lWeapons = []
        self.bag = None
        self.weapon_select = 1

        self.next_allowed_shot =[0 for _ in range(NBRWEAPONSTOCK)]

        self.spell_hold=None

        self.init_lWeapons()

        self.text_name = ["Sac","J","K","L"]

        self.complete_info = CompleteInfo(screen_size,cell_size)

        #self.icone_size = size.CELL_SIZE*4

    def init_lWeapons(self):

        for _ in range(NBRWEAPONSTOCK):
            self.lWeapons.append(None)

    def add_weapon(self,i,id_weapon,nbr_spell_max,spells_id,screen_size):

        #if id_weapon == 0:
        #    #print("Create Bag") #Done only 1 time
        #    self.bag = Weapon(id_weapon,nbr_spell_max,spells_id,i,screen_size)
        #
        #else :
        self.lWeapons[i] = Weapon(id_weapon,nbr_spell_max,spells_id,i,screen_size,self.text_name[i])

    def draw_spells(self,screen,screen_size,mouse_pos):

        spell_touch = None
        weapon_hold = None

        for j in range(len(self.lWeapons)) :

            #y = self.return_posy_blit_weapon(screen_size,i)
#
            #x_spells=[]

            #for j in range(len(self.lWeapons[i].spells_id)):
            #    x_spells.append(self.return_posx_blit_spell(screen_size,j))
            new_spell = self.lWeapons[j].draw_spells(screen,screen_size,j,mouse_pos) #+1 car il doit d'abord
            
            if new_spell !=None and new_spell.img!=None :#Check si il y a bien un spell
                spell_touch = new_spell

            if spell_touch==None and weapon_hold == None and self.check_mouse_touch_weapon(mouse_pos,self.lWeapons[j]):
                weapon_hold = self.lWeapons[j]

        if self.spell_hold==None:

            self.complete_info.blit_info(screen,spell_touch,weapon_hold)

    def check_mouse_touch_weapon(self,mouse_pos,weapon):

        if weapon.pos_text[0] - weapon.icone_size < mouse_pos[0] and mouse_pos[0] < weapon.pos_text[0] + weapon.icone_size:
   
            if weapon.pos_text[1] - weapon.icone_size < mouse_pos[1] and mouse_pos[1] < weapon.pos_text[1] + weapon.icone_size:

                return True
        return False

    def update_next_allowed_shot(self,delta_time,id_weapon):

        now = time.perf_counter()

        self.next_allowed_shot[id_weapon] = now+delta_time/1000

        self.lWeapons[id_weapon].timer.update_delta_time(now,delta_time/1000)

    def shot(self,id_key):

        now = time.perf_counter()

        if now >= self.next_allowed_shot[id_key] :

            return [6,id_key]
        
        else :
            return #[6,angle] #Si tu veux plus avoir de contraite de tir niveau client
        
    def touch_spells(self,mouse_pos):

        for weapon in (self.lWeapons):

            for spell in (weapon.spells) :

                #if spell.spell_id!=0 :

                    #print("touch",spell.rect.collidepoint(mouse_pos),mouse_pos)

                if spell.rect.collidepoint(mouse_pos) :

                    
                    return self.trigger_spell_touch(spell)
                
        #No collision = throw the spell

        spell_previous_old = self.spell_hold
                
        if self.spell_hold :
            self.spell_hold.blit_icone = True
            
        self.spell_hold = None
                
        return -1,spell_previous_old,None #No collision
    
    def throw_spell(self,spell):

        self.lWeapons[spell.idx_weapon].spells[spell.idx_spell].img = None
                    
    def trigger_spell_touch(self,spell):

        if self.spell_hold==None :
            if spell.img!=None:
                self.spell_hold=spell
                spell.blit_icone = False

                return 0,spell.img,None

            else :
                return -1,None,None

        else :
            spell_1_info = spell.idx_weapon,spell.idx_spell
            spell_2_info = self.spell_hold.idx_weapon,self.spell_hold.idx_spell
            self.switch_spell(self.spell_hold,spell)
            self.spell_hold.blit_icone = True
            self.spell_hold=None

            return 1,spell_1_info,spell_2_info

    def switch_spell(self,spell_1,spell_2):
            
            
            self.lWeapons[spell_1.idx_weapon].spells[spell_1.idx_spell] = spell_2
            self.lWeapons[spell_2.idx_weapon].spells[spell_2.idx_spell] = spell_1
            
            spell_1.idx_weapon,spell_2.idx_weapon = spell_2.idx_weapon,spell_1.idx_weapon
            spell_1.idx_spell,spell_2.idx_spell = spell_2.idx_spell,spell_1.idx_spell
            spell_1.pos_x,spell_2.pos_x = spell_2.pos_x,spell_1.pos_x
            spell_1.pos_y,spell_2.pos_y = spell_2.pos_y,spell_1.pos_y

            spell_1.load_rect()
            spell_2.load_rect()

    def stop_holding_spell(self):
        self.spell_hold.blit_icone = True
        self.spell_hold=None
            
    def draw_timer_all(self,screen):
        
        for weapon in self.lWeapons :

            weapon.draw_timer(screen,time.perf_counter())

    def reduce_time(self,id_weapon):

        self.complete_info.reduce_time(id_weapon)