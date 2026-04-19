from shared.constants import world
from serv.domain.objects.object_type import spell_on_ground,healer_respawn

class objects_manager:

    def __init__(self):

        self.chunk_objects = {}
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

    def add_object(self,ele_idx,id_categorie,pos_x,pos_y,chunk,price):

        id = self.generate_id()

        if ele_idx=="SPELL":

            ele = spell_on_ground(id_categorie,pos_x,pos_y,price)

            self.chunk_objects[chunk][id] = ele

            return id,ele
        
        elif ele_idx=="HEALER":

            ele = healer_respawn(id_categorie,pos_x,pos_y,price)

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


