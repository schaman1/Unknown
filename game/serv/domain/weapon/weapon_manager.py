from shared.constants.world import NBRWEAPONSTOCK
from serv.domain.weapon.weapon1 import Weapon1,WeaponBag

class WeaponManager :

    def __init__(self):

        self.lWeapons = []
        #self.bag = WeaponBag()

        self.weapon_select = 1
        self.id_event_player_do = [] #Each frame player do events base on the list of id and reset  it (ex: if 1 in dahs then remove 1 from list)

        self.init_lWeapons()

    def init_lWeapons(self):


        for i in range(NBRWEAPONSTOCK):

            if 0==i:

                self.lWeapons.append(WeaponBag())
            else :
                self.lWeapons.append(Weapon1())

    def return_all_weapon(self):

        res = []

        for i,weapon in enumerate(self.lWeapons):
            res.append(weapon.return_info(i))

        return res
    
    def return_weapon_select(self):

        return self.lWeapons[self.weapon_select]
    
    def create_shot(self,id_weapon,pos,angle):

        angle=angle*90

        res = self.lWeapons[id_weapon].trigger_shot(angle,pos)
        
        if res==None :
            projectiles,events = None,None
        
        else :

            projectiles,events = res[0],res[1]


            self.id_event_player_do+=events

        return projectiles