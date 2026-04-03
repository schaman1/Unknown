from shared.constants import world
from client.config.size_display import CELL_SIZE
from client.ui.objects.spell_on_ground import spell_on_ground

class objects_manager:

    def __init__(self,cell_size):

        self.cell_size = cell_size

        self.chunk_objects = {}

        self.init_dico_dic_objects()

    def init_dico_dic_objects(self):
        for i in range(world.LEN_Y_CHUNK) :
            for j in range(world.LEN_Y_CHUNK) :
                self.chunk_objects[i*100+j] = {}

    def add_object(self,type,id,img,pos_x,pos_y,price,chunk):

        if type==world.TYPE_OBJECT["SPELL"]:

            pos_x,pos_y = self.convert_pos(pos_x,pos_y)

            self.chunk_objects[chunk][id] = spell_on_ground(img,pos_x,pos_y,price)

    def convert_pos(self,x,y):

        x = self.convert_from_base(x*self.cell_size)
        y = self.convert_from_base(y*self.cell_size)

        return x,y

    def blit_object(self,element,screen,x,y):
        """Blit le monstre avec l'id id_objects sur le canva des monstres"""
        element.blit(screen,x,y)
    
    def blit_all_objects(self,screen,x,y):
        """Blit tout les monstres sur le canva des monstres"""

        for pos in self.chunk_objects :
            for id_objects in self.chunk_objects[pos] :

                self.blit_object(self.chunk_objects[pos][id_objects],screen,x,y)

    def convert_from_base(self,i):

        return i//world.RATIO