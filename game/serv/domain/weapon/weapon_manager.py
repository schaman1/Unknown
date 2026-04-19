from shared.constants.world import NBRWEAPONSTOCK
from serv.domain.weapon.weapon1 import WeaponBag,Weapon1,Weapon2,Weapon3

class WeaponManager :

    def __init__(self,team):

        self.lWeapons = []
        #self.bag = WeaponBag()

        self.weapon_select = 1

        self.init_lWeapons(team)

    def bag_not_full(self):
        return self.lWeapons[0].not_full()

    def add_spell(self,id,id_weapon):
        return self.lWeapons[id_weapon].add_spell(id)

    def init_lWeapons(self,team):

        for i in range(NBRWEAPONSTOCK):

            if i==0:

                self.lWeapons.append(WeaponBag(team))
        
            elif i==1 :
                self.lWeapons.append(Weapon1(team))

            elif i==2 :
                self.lWeapons.append(Weapon2(team))
            
            elif i==3 :
                self.lWeapons.append(Weapon3(team))

            else :
                self.lWeapons.append(Weapon1(team))

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

        return projectiles,events