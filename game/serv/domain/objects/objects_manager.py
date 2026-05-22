from shared.constants import world
from serv.domain.objects.object_type import spell_on_ground,healer_respawn,upgrade_size_weapon,Chest,upgrade_life
import random

class objects_manager:

    def __init__(self):

        self.chunk_objects = {}
        self.upgrades = {"UpgradeWeapon":upgrade_size_weapon,
                         "UpgradeLife":upgrade_life,
                         "UpgradeWeapon2":upgrade_size_weapon}
        self.id_curr = 0

        self.init_dico_dic_objects()

    def generate_id(self):

        id = self.id_curr

        self.id_curr = (self.id_curr+1)%256

        return id

    def init_dico_dic_objects(self):
        for i in range(world.LEN_Y_CHUNK) :
            for j in range(world.LEN_Y_CHUNK) :
                self.chunk_objects[i*100+j] = {}

    def add_object(self,ele_idx,id_categorie,pos_x,pos_y,chunk,price): #Categorie is used for chest

        id = self.generate_id()

        if ele_idx=="SPELL":

            ele = spell_on_ground(id_categorie,pos_x,pos_y,price)

            self.chunk_objects[chunk][id] = ele

            return id,ele
        
        elif ele_idx=="HEALER":

            ele = healer_respawn(id_categorie,pos_x,pos_y,price)

            self.chunk_objects[chunk][id] = ele

            return id,ele
        
        elif ele_idx=="UpgradeWeapon":

            ele = upgrade_size_weapon(id_categorie,pos_x,pos_y,price)

            self.chunk_objects[chunk][id] = ele

            return id,ele
        
        elif ele_idx=="UpgradeLife":

            ele = upgrade_life(id_categorie,pos_x,pos_y,price)

            self.chunk_objects[chunk][id] = ele

            return id,ele
        
        elif ele_idx=="Chest":

            ele = Chest(id_categorie,pos_x,pos_y,price)

            self.chunk_objects[chunk][id] = ele

            return id,ele
        
        else :
            print("Unknown type in add_object")
            return None
        
    def destroy_object(self,chunk,id):

        del self.chunk_objects[chunk][id]
        
    def trigger(self,chunk,id,player):

        element = self.chunk_objects[chunk][id]

        if player.money>=element.price and player.can_pick_spell():

            player.update_money(-element.price)

            if element.unique_use :
                self.destroy_object(chunk,id)

            return element.trigger_value,chunk,id,element
        
    def spawn_random_spell(self,cat,chunk,x,y):

        if cat == 0 : #Means all

            return
        
        elif cat == 1: #Means spell_low_quality

            id = self.generate_id()
            spell = spell_on_ground(None,x,y,0,randomize=True,rarity="common")

            self.chunk_objects[chunk][id] = spell

            return id,spell,"SPELL"
        
        elif cat == 2: #Means special = Upgade weapon

            id = self.generate_id()

            name = random.choice(list(self.upgrades.keys()))

            id_cat = 1
            if name == "UpgradeWeapon2":
                id_cat = 2
                name = "UpgradeWeapon"

            upgrade = self.upgrades[name](id_cat,x,y,0)

            self.chunk_objects[chunk][id] = upgrade

            return id,upgrade,name
        
        elif cat == 3: #Means Rare spell

            id = self.generate_id()
            spell = spell_on_ground(None,x,y,0,randomize=True,rarity="rare")

            self.chunk_objects[chunk][id] = spell

            return id,spell,"SPELL"
        
        elif cat == 4:

            id = self.generate_id()
            spell = spell_on_ground(None,x,y,0,randomize=True,rarity="legendary")

            self.chunk_objects[chunk][id] = spell

            return id,spell,"SPELL"
