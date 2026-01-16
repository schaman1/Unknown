from serv.config import weapons
from shared.constants.world import NBRWEAPONSTOCK
from serv.domain.weapon.weapon1 import Weapon1

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
            res.append([10,i,weapon.return_info()])

        return res
    
    def return_weapon_select(self):

        return self.lWeapons[self.weapon_select]
