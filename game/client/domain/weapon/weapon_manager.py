from shared.constants.world import NBRWEAPONSTOCK
from client.domain.weapon.weapon import Weapon
import time

class WeaponManager:

    def __init__(self):

        self.lWeapons = []
        self.weapon_select = 0

        self.next_allowed_shot = 0

        self.init_lWeapons()

    def init_lWeapons(self):

        for _ in range(NBRWEAPONSTOCK):
            self.lWeapons.append(None)

    def add_weapon(self,i,id_weapon,nbr_spell_max,spells_id):

        self.lWeapons[i] = Weapon(id_weapon,nbr_spell_max,spells_id)

    def draw_weapon(self,screen,angle,pos_player, frame):

        self.lWeapons[self.weapon_select].draw(screen,angle,pos_player, frame)


    def draw_icone_weapon(self,screen,screen_size):

        for i in range(len(self.lWeapons)) :

            self.lWeapons[i].draw_icone(screen,screen_size,i)

    def update_next_allowed_shot(self,delta_time):

        self.next_allowed_shot = time.perf_counter()+delta_time/1000

    def shot(self,angle):

        now = time.perf_counter()

        if now >= self.next_allowed_shot :

            return [4,angle]
        
        else :
            return #[4,angle] #Si tu veux plus avoir de contraite de tir niveau client