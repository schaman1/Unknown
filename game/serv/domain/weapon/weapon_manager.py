from shared.constants.world import NBRWEAPONSTOCK
from serv.domain.weapon.weapon1 import Weapon1
import time

class WeaponManager :

    def __init__(self):

        self.lWeapons = []

        self.weapon_select = 0

        self.init_lWeapons()

    def init_lWeapons(self):

        for _ in range(NBRWEAPONSTOCK):

            self.lWeapons.append(Weapon1())

    def return_all_weapon(self):

        res = []

        for i,weapon in enumerate(self.lWeapons):
            res.append(weapon.return_info(i))

        return res
    
    def return_weapon_select(self):

        return self.lWeapons[self.weapon_select]
    
    def create_shot(self,angle,pos):

        projectiles = self.lWeapons[self.weapon_select].create_projectile(angle,pos)

        return projectiles