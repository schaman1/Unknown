from shared.constants.world import NBRWEAPONSTOCK

class WeaponManager:

    def __init__(self):

        self.lWeapons = []
        self.weapon_select = 0

    def init_lWeapons(self):

        for _ in range(NBRWEAPONSTOCK):
            self.lWeapons.append(None)