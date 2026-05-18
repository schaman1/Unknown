from serv.domain.objects.interactable_object import interactable_object
from serv.domain.weapon import upgrades
import random

class spell_on_ground(interactable_object):

    def __init__(self,id_categorie,pos_x,pos_y,price=0,randomize = False):

        if randomize : 
            id_categorie = random.choice(list(upgrades.UPGRADES.keys()))

        super().__init__(id_categorie,pos_x,pos_y,price)

        self.trigger_value = "AddToInventaire"

class healer_respawn(interactable_object):

    def __init__(self,id_categorie,pos_x,pos_y,price=0):

        super().__init__(id_categorie,pos_x,pos_y,price,unique_use=False)

        self.trigger_value = "Heal"

class upgrade_size_weapon(interactable_object):

    def __init__(self,id_categorie,pos_x,pos_y,price=0):

        super().__init__(id_categorie,pos_x,pos_y,price)

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