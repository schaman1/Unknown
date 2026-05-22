from serv.config import weapons
from serv.domain.weapon.base_weapon import Weapon
from serv.config.add_objects_begin import WEAPONS_BEGIN
from serv.domain.weapon import upgrades

class WeaponBag(Weapon):

    def __init__(self,team,player):

        super().__init__(
            refill_time = 0,
            spell_time= 0,
            nbr_slot = weapons.WEAPON_BAG_NBR_SLOT,
            nbr_upgrades_trigger = 0,
            id = weapons.ID_WEAPON_BAG,
            team=team,
            player=player
        )

        self.init_slot()

    def not_full(self):
        idx = 0

        while idx<self.nbr_slot and self.spells_on_shot[idx]!=None:
            idx+=1

        if idx==self.nbr_slot :
            return False
        
        return True

    def add_spell(self,id):

        idx = 0

        while idx<self.nbr_slot and self.spells_on_shot[idx]!=None:
            idx+=1

        if idx<self.nbr_slot :
            self.fill_slot(idx,upgrades.UPGRADES[id])

            return idx
    
        return None

    def init_slot(self):

        id = 0
        for idx in WEAPONS_BEGIN[0] :

            self.fill_slot(id,upgrades.UPGRADES[idx])
            id+=1

class Weapon1(Weapon) :

    def __init__(self,team,player):

        super().__init__(
            refill_time = weapons.REFILL_TIME_WEAPON1,
            spell_time= weapons.SPELL_TIME_WEAPON1,
            nbr_slot = weapons.NBR_SLOT_WEAPON1,
            nbr_upgrades_trigger = weapons.NBR_UPGRADES_TRIGGER_WEAPON1,
            id = weapons.ID_WEAPON1,
            team=team,
            player=player
        )

        self.init_slot()

    def init_slot(self):
        id = 0
        for idx in WEAPONS_BEGIN[1] :

            self.fill_slot(id,upgrades.UPGRADES[idx])
            id+=1

class Weapon2(Weapon) :

    def __init__(self,team,player):

        super().__init__(
            refill_time = weapons.REFILL_TIME_WEAPON1,
            spell_time= weapons.SPELL_TIME_WEAPON1,
            nbr_slot = weapons.NBR_SLOT_WEAPON1,
            nbr_upgrades_trigger = weapons.NBR_UPGRADES_TRIGGER_WEAPON1,
            id = weapons.ID_WEAPON1,
            team=team,
            player=player
        )

        self.init_slot()

    def init_slot(self):
        id = 0
        for idx in WEAPONS_BEGIN[2] :

            self.fill_slot(id,upgrades.UPGRADES[idx])
            id+=1
class Weapon3(Weapon) :

    def __init__(self,team,player):

        super().__init__(
            refill_time = weapons.REFILL_TIME_WEAPON1,
            spell_time= weapons.SPELL_TIME_WEAPON1,
            nbr_slot = weapons.NBR_SLOT_WEAPON1,
            nbr_upgrades_trigger = weapons.NBR_UPGRADES_TRIGGER_WEAPON1,
            id = weapons.ID_WEAPON1,
            team=team,
            player=player
        )

        self.init_slot()

    def init_slot(self):
        id = 0
        for idx in WEAPONS_BEGIN[3] :

            self.fill_slot(id,upgrades.UPGRADES[idx])
            id+=1

class WeaponLaseroide(Weapon):

    def __init__(self,team,player):

        super().__init__(
            refill_time = weapons.REFILL_TIME_LASEROIDE,
            spell_time= weapons.SPELL_TIME_LASEROIDE,
            nbr_slot = weapons.NBR_SLOT_LASEROIDE,
            nbr_upgrades_trigger = weapons.NBR_UPGRADES_TRIGGER_LASEROIDE,
            id = -1,   #on s'en fiche normalement
            team=team,
            player=player
        )

        self.min_delay = self.loading_time_spell
        self.init_slot()

    def init_slot(self):

        for i in range(self.nbr_slot) :
            self.fill_slot(i,upgrades.CreateLaser())


class WeaponLimace(Weapon):
    def __init__(self, team, player) :
        super().__init__(
            refill_time= weapons.RELOAD_LIMACE,
            spell_time= weapons.SPELL_TIME_LIMACE,
            nbr_slot = weapons.NBR_MUNITIONS,
            nbr_upgrades_trigger = weapons.NBR_UPGRADES_TRIGGER_LIMACE,
            id = -2, team = team, player = player
        )
        
        self.init_slot()

    def init_slot(self):
        # return
        for i in range(self.nbr_slot):
            self.fill_slot(i, upgrades.CreateStone())

