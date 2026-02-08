from shared.constants.world import NBRWEAPONSTOCK
from serv.domain.weapon.weapon1 import Weapon1,WeaponBag

class WeaponManager :

    def __init__(self):

        self.lWeapons = []
        #self.bag = WeaponBag()

        self.weapon_select = 1

        self.init_lWeapons()

    def init_lWeapons(self):


        for i in range(NBRWEAPONSTOCK):

            if 0==i:

                self.lWeapons.append(WeaponBag())
            else :
                self.lWeapons.append(Weapon1())

    def return_all_weapon(self):

        res = []

        #res.append(self.bag.return_info(0))

        for i,weapon in enumerate(self.lWeapons):
            res.append(weapon.return_info(i))

        return res
    
    def return_weapon_select(self):

        return self.lWeapons[self.weapon_select]
    
    def create_shot(self,angle,pos):

        projectiles = self.lWeapons[self.weapon_select].trigger_shot(angle,pos)

        return projectiles