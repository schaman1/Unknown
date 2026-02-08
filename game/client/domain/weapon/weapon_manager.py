from shared.constants.world import NBRWEAPONSTOCK
from client.domain.weapon.weapon import Weapon
#from client.config import size_display as size
import time

class WeaponManager:

    def __init__(self):

        self.lWeapons = []
        self.bag = None
        self.weapon_select = 1

        self.next_allowed_shot = 0

        self.spell_hold=None

        self.init_lWeapons()

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
        self.lWeapons[i] = Weapon(id_weapon,nbr_spell_max,spells_id,i,screen_size)

    def draw_weapon(self,screen,angle,pos_player, frame):

        self.lWeapons[self.weapon_select].draw(screen,angle,pos_player,frame)

    def draw_icone_weapon(self,screen,screen_size):

        return #Enleve les weapon dessiné a dessus de la barre de vie
        for i in range(len(self.lWeapons)) :

            self.lWeapons[i].draw_icone(screen,screen_size,i)

    def draw_spells(self,screen,screen_size):

        for j in range(len(self.lWeapons)) :

            #y = self.return_posy_blit_weapon(screen_size,i)
#
            #x_spells=[]

            #for j in range(len(self.lWeapons[i].spells_id)):
            #    x_spells.append(self.return_posx_blit_spell(screen_size,j))

            self.lWeapons[j].draw_spells(screen,screen_size,j) #+1 car il doit d'abord

    def update_next_allowed_shot(self,delta_time):

        self.next_allowed_shot = time.perf_counter()+delta_time/1000

    def shot(self,angle):

        now = time.perf_counter()

        if now >= self.next_allowed_shot :

            return [4,angle]
        
        else :
            return #[4,angle] #Si tu veux plus avoir de contraite de tir niveau client
        
    def touch_spells(self,mouse_pos):

        for weapon in (self.lWeapons):

            for spell in (weapon.spells) :

                #if spell.spell_id!=0 :

                    #print("touch",spell.rect.collidepoint(mouse_pos),mouse_pos)

                if spell.rect.collidepoint(mouse_pos) :

                    
                    return self.trigger_spell_touch(spell)
                
        return -1,None,None #No collision
                    

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
            img_1 = spell_1.img
            spell_1.img=spell_2.img
            spell_2.img=img_1

    def stop_holding_spell(self):
        self.spell_hold.blit_icone = True
        self.spell_hold=None
            