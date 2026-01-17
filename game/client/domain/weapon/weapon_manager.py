from shared.constants.world import NBRWEAPONSTOCK
from client.domain.weapon.weapon import Weapon

class WeaponManager:

    def __init__(self):

        self.lWeapons = []
        self.weapon_select = 0

    def init_lWeapons(self):

        for _ in range(NBRWEAPONSTOCK):
            self.lWeapons.append(None)

    def add_weapon(self,i,id_weapon,loading_time,nbr_spell_max):

        self.lWeapons[i] = Weapon(id_weapon,loading_time,nbr_spell_max)

    def draw_weapon(self,screen,mouse_pos,center):

        self.lWeapons[self.weapon_select].draw(screen,mouse_pos,center)