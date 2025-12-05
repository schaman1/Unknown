import pygame
import var
from client.Monster_client.C_monster import Skeleton

class Monster_all :

    def __init__(self,cell_size,canva_size):

        self.dic_monster = {} #Liste des monstres dans la map
        self.init_dico_dic_monsters(canva_size)
        self.cell_size = cell_size

    def init_dico_dic_monsters(self,canva_size):
        for i in range(canva_size[0]//var.SIZE_CHUNK_MONSTER+1) :
            for j in range(canva_size[1]//var.SIZE_CHUNK_MONSTER+1) :
                self.dic_monster[i*100+j] = {}

    def init_monster(self,lchunck_monsters,screen):
        """Initialise les monstres reçus du serv"""

        for (chunk, id, x, y) in lchunck_monsters :
            self.dic_monster[chunk][id] = Skeleton(x,y,chunk)

            self.blit_monster(self.dic_monster[chunk][id],screen)

    def blit_monster(self,monster,screen):
        """Blit le monstre avec l'id id_monster sur le canva des monstres"""
        screen.blit(monster.Img, self.calculate_pos_blit(monster))

    def calculate_pos_blit(self,monster):
        x = monster.pos_x * self.cell_size - monster.width//2
        y = monster.pos_y * self.cell_size - monster.height
        return (x,y)
    
    def blit_all_monster(self,screen):
        """Blit tout les monstres sur le canva des monstres"""

        for pos in self.dic_monster :
            for id_monster in self.dic_monster[pos] :
                self.blit_monster(self.dic_monster[pos][id_monster],screen)