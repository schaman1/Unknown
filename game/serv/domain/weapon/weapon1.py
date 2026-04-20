from serv.config import weapons
from serv.domain.weapon.base_weapon import Weapon
from serv.domain.weapon import upgrades

class WeaponBag(Weapon):

    def __init__(self,team):

        super().__init__(
            refill_time = 0,
            spell_time= 0,
            nbr_slot = weapons.WEAPON_BAG_NBR_SLOT,
            nbr_upgrades_trigger = 0,
            id = weapons.ID_WEAPON_BAG,
            team=team
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

        self.fill_slot(0,upgrades.DoubleSpell())
        #self.fill_slot(1,upgrades.CreateFire())
        #self.fill_slot(2,upgrades.CreateMagic())

class Weapon1(Weapon) :

    def __init__(self,team):

        super().__init__(
            refill_time = weapons.REFILL_TIME_WEAPON1,
            spell_time= weapons.SPELL_TIME_WEAPON1,
            nbr_slot = weapons.NBR_SLOT_WEAPON1,
            nbr_upgrades_trigger = weapons.NBR_UPGRADES_TRIGGER_WEAPON1,
            id = weapons.ID_WEAPON1,
            team=team
        )

        self.init_slot()

    def init_slot(self):
        self.fill_slot(0,upgrades.SmallDash())
        self.fill_slot(1,upgrades.LongDash())
        #self.fill_slot(2,upgrades.LongDash())
        #self.fill_slot(2,upgrades.CreateFire())

class Weapon2(Weapon) :

    def __init__(self,team):

        super().__init__(
            refill_time = weapons.REFILL_TIME_WEAPON1,
            spell_time= weapons.SPELL_TIME_WEAPON1,
            nbr_slot = weapons.NBR_SLOT_WEAPON1,
            nbr_upgrades_trigger = weapons.NBR_UPGRADES_TRIGGER_WEAPON1,
            id = weapons.ID_WEAPON1,
            team=team
        )

        self.init_slot()

    def init_slot(self):
        self.fill_slot(0,upgrades.CreateFire())
        self.fill_slot(1,upgrades.CreateFire())

class Weapon3(Weapon) :

    def __init__(self,team):

        super().__init__(
            refill_time = weapons.REFILL_TIME_WEAPON1,
            spell_time= weapons.SPELL_TIME_WEAPON1,
            nbr_slot = weapons.NBR_SLOT_WEAPON1,
            nbr_upgrades_trigger = weapons.NBR_UPGRADES_TRIGGER_WEAPON1,
            id = weapons.ID_WEAPON1,
            team=team
        )

        self.init_slot()

    def init_slot(self):
        self.fill_slot(0,upgrades.CreateLune())
