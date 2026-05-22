from serv.domain.objects.interactable_object import interactable_object
from serv.domain.weapon import upgrades
import random

class spell_on_ground(interactable_object):

    def __init__(self,id_categorie,pos_x,pos_y,price=0,randomize = False,rarity = "common"):

        if randomize : 

            if rarity == "common" :
                id_categorie = random.choice(upgrades.common_upgrades)
            elif rarity == "rare":
                id_categorie = random.choice(upgrades.rare_upgrades)
            elif rarity == "legendary":
                id_categorie = random.choice(upgrades.legendary_upgrades)

        super().__init__(id_categorie,pos_x,pos_y,price)

        self.trigger_value = "AddToInventaire"

class healer_respawn(interactable_object):

    def __init__(self,id_categorie,pos_x,pos_y,price=0):

        super().__init__(id_categorie,pos_x,pos_y,price,unique_use=False)

        self.trigger_value = "Heal"

class upgrade_size_weapon(interactable_object):

    def __init__(self,id_categorie,pos_x,pos_y,price=0):

        super().__init__(id_categorie,pos_x,pos_y,price)
        #Id categorie = 1 or 2. 2 means +2 slot ! 1 = +1 slot !

        self.trigger_value = "UpgradeWeapon"

class upgrade_life(interactable_object):

    def __init__(self,id_categorie,pos_x,pos_y,price=0):

        super().__init__(id_categorie,pos_x,pos_y,price,power = 50)

        self.trigger_value = "UpgradeLife"

class Chest(interactable_object):

    def __init__(self,id_categorie,pos_x,pos_y,price=0):

        super().__init__(id_categorie,pos_x,pos_y,price)

        self.open = False

        self.trigger_value = "OpenChest"