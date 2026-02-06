from shared.constants.world import NBRWEAPONSTOCK
from client.domain.weapon.weapon import Weapon
#from client.config import size_display as size
import time

class WeaponManager:

    def __init__(self):

        self.lWeapons = []
        self.weapon_select = 0

        self.next_allowed_shot = 0

        self.init_lWeapons()

        #self.icone_size = size.CELL_SIZE*4

    def init_lWeapons(self):

        for _ in range(NBRWEAPONSTOCK):
            self.lWeapons.append(None)

    def add_weapon(self,i,id_weapon,nbr_spell_max,spells_id,screen_size):

        self.lWeapons[i] = Weapon(id_weapon,nbr_spell_max,spells_id,i,screen_size)

    def draw_weapon(self,screen,angle,pos_player, frame):

        self.lWeapons[self.weapon_select].draw(screen,angle,pos_player, frame)

    def draw_icone_weapon(self,screen,screen_size):

        for i in range(len(self.lWeapons)) :

            self.lWeapons[i].draw_icone(screen,screen_size,i)

    def draw_spells(self,screen,screen_size):

        for i in range(len(self.lWeapons)) :

            #y = self.return_posy_blit_weapon(screen_size,i)
#
            #x_spells=[]

            #for j in range(len(self.lWeapons[i].spells_id)):
            #    x_spells.append(self.return_posx_blit_spell(screen_size,j))


            self.lWeapons[i].draw_spells(screen,screen_size,i)

    def update_next_allowed_shot(self,delta_time):

        self.next_allowed_shot = time.perf_counter()+delta_time/1000

    def shot(self,angle):

        now = time.perf_counter()

        if now >= self.next_allowed_shot :

            return [4,angle]
        
        else :
            return #[4,angle] #Si tu veux plus avoir de contraite de tir niveau client
        
    #def return_posy_blit_weapon(self,screen_size,i):
#
    #    return screen_size[1]/10+2*i*(self.icone_size)
#
    #def return_posx_blit_spell(self,screen_size,i):
    #    padding = screen_size[0]/50
#
    #    return screen_size[0]//4 + padding + self.icone_size * i
