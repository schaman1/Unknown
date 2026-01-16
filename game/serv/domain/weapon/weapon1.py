from serv.config import weapons
from serv.domain.weapon.base_weapon import Weapon
from serv.domain.weapon import upgrades


class Weapon1(Weapon) :

    def __init__(self):

        super().__init__(
            loading_time = weapons.LOAD_WEAPON1,
            nbr_slot = weapons.NBR_SLOT_WEAPON1,
            nbr_upgrades_trigger = weapons.NBR_UPGRADES_TRIGGER_WEAPON1,
            id = weapons.ID_WEAPON1
        )

        self.init_slot()

    def init_slot(self):
        self.fill_slot(0,upgrades.create_fireball)
        self.fill_slot(1,upgrades.add_speed)
        self.fill_slot(2,upgrades.create_fireball)
    
    def fill_slot(self,idx,function):

        self.spells_on_shot[idx]=function
