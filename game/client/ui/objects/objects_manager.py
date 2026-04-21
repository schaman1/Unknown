from shared.constants import world
#from client.config.size_display import CELL_SIZE
from client.ui.objects.object_type import spell_on_ground,healer_spawn
import pygame
import math

class objects_manager:

    def __init__(self,cell_size):

        self.cell_size = cell_size

        self.distance_max_trigger = world.NBR_CELL_CAN_SEE*cell_size

        self.interact_img = pygame.image.load("assets/ui/infos/interact.png")
        self.interact_img = pygame.transform.scale(self.interact_img,(10*cell_size,1*cell_size))

        self.chunk_objects = {}

        self.init_dico_dic_objects()

    def init_dico_dic_objects(self):
        for i in range(world.LEN_Y_CHUNK) :
            for j in range(world.LEN_Y_CHUNK) :
                self.chunk_objects[i*100+j] = {}

    def add_object(self,type,id,img,pos_x,pos_y,chunk,price):

        if type==world.TYPE_OBJECT["SPELL"]:

            pos_x,pos_y = self.convert_pos(pos_x,pos_y)

            self.chunk_objects[chunk][id] = spell_on_ground(img,pos_x,pos_y,price)


        elif type==world.TYPE_OBJECT["HEALER"]:

            pos_x,pos_y = self.convert_pos(pos_x,pos_y)

            self.chunk_objects[chunk][id] = healer_spawn(img,pos_x,pos_y,price)


    def destroy_object(self,chunk,id):

        del self.chunk_objects[chunk][id]

    def convert_pos(self,x,y):

        x = self.convert_from_base(x*self.cell_size)
        y = self.convert_from_base(y*self.cell_size)

        return x,y

    def blit_object(self,element,screen,x,y):
        """Blit le monstre avec l'id id_objects sur le canva des monstres"""

        element.blit(screen,x,y)
    
    def blit_all_objects(self,screen,x,y,pos_player):
        """Blit tout les monstres sur le canva des monstres"""

        for pos in self.chunk_objects :
            for id_objects in self.chunk_objects[pos] :

                dist = self.distance(pos_player,self.chunk_objects[pos][id_objects])

                self.blit_object(self.chunk_objects[pos][id_objects],screen,x,y)

                if dist<self.distance_max_trigger:

                    self.blit_interact_info(screen,self.chunk_objects[pos][id_objects],x,y)

    def blit_interact_info(self,screen,element,x,y):
        
        pos_x = element.pos_x +x  - 5*self.cell_size
        pos_y = element.pos_y +y - self.cell_size*1 - element.size_img[1]//2

        screen.blit(self.interact_img,(pos_x,pos_y))

    def convert_from_base(self,i):

        return i//world.RATIO
    
    def distance(self,pos_player,element):

        dist = (pos_player[0]-element.pos_x)**2 + (pos_player[1]-element.pos_y)**2
        return math.sqrt(dist)
    
    def test_trigger(self,pos_player): #To opti

        nearest_el = [self.distance_max_trigger,None]

        for chunk in self.chunk_objects.keys() :

            for id,element in self.chunk_objects[chunk].items():

                dist = self.distance(pos_player,element)

                if dist<nearest_el[0] :

                    nearest_el = [dist,[chunk,id]]
                
        return nearest_el