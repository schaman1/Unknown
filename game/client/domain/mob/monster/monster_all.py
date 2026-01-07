from shared.constants import world
from client.domain.mob.monster.monster import Skeleton

class Monster_all :

    def __init__(self,cell_size,canva_size):

        self.dic_monster = {} #Liste des monstres dans la map
        self.init_dico_dic_monsters(canva_size)
        self.cell_size = cell_size

    def init_dico_dic_monsters(self,canva_size):
        for i in range(canva_size[0]//world.SIZE_CHUNK_MONSTER+1) :
            for j in range(canva_size[1]//world.SIZE_CHUNK_MONSTER+1) :
                self.dic_monster[i*100+j] = {}

    def init_monster(self,lchunck_monsters):
        """Initialise les monstres reçus du serv"""

        for (chunk, id, x, y) in lchunck_monsters :
            self.dic_monster[chunk][id] = Skeleton(x,y,chunk,self.cell_size)

    def blit_monster(self,monster,screen,x,y):
        """Blit le monstre avec l'id id_monster sur le canva des monstres"""
        monster.blit(screen,x,y)
    
    def blit_all_monsters(self,screen,x,y):
        """Blit tout les monstres sur le canva des monstres"""

        for pos in self.dic_monster :
            for id_monster in self.dic_monster[pos] :
                self.blit_monster(self.dic_monster[pos][id_monster],screen,x,y)