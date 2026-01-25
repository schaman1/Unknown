from serv.config import weapons
from serv.domain.weapon.base_weapon import Weapon
from serv.domain.weapon import upgrades


class Weapon1(Weapon) :

    def __init__(self):

        super().__init__(
            refill_time = weapons.REFILL_TIME_WEAPON1,
            spell_time= weapons.SPELL_TIME_WEAPON1,
            nbr_slot = weapons.NBR_SLOT_WEAPON1,
            nbr_upgrades_trigger = weapons.NBR_UPGRADES_TRIGGER_WEAPON1,
            id = weapons.ID_WEAPON1
        )

        self.init_slot()

    def init_slot(self):
        self.fill_slot(0,upgrades.CreateFire())
        self.fill_slot(1,upgrades.CreateFire())
        self.fill_slot(2,upgrades.CreateFire())

    def fill_slot(self,idx,function):

        if idx >= len(self.spells_on_shot):
            print("Unable to fill spot in weapon bcs idx tooo high")

        else :
            self.spells_on_shot[idx]=function
