import pygame
from client.Monster_client.C_monster import Skeleton

class Monster_all :

    def __init__(self,cell_size,canva_size):

        self.list_monster = {} #Liste des monstres dans la map
        self.cell_size = cell_size
        self.canva_monster = pygame.Surface((canva_size[0]*cell_size,canva_size[1]*cell_size), pygame.SRCALPHA)

    def init_monster(self,lchunck_monster):
        """Initialise les monstres reçus du serv"""

        for pos,chunck in lchunck_monster.items() :
            self.list_monster[pos] = {}

            for monster in chunck :
                if monster[3] == "Skeleton" :
                    self.list_monster[pos][monster[0]] = Skeleton(monster[1],monster[2],pos)
                    self.blit_monster(self.list_monster[pos][monster[0]])

    def blit_monster(self,monster):
        """Blit le monstre avec l'id id_monster sur le canva des monstres"""
        self.canva_monster.blit(monster.Img, self.calculate_pos_blit(monster))

    def calculate_pos_blit(self,monster):
        x = monster.pos_x * self.cell_size - monster.width//2
        y = monster.pos_y * self.cell_size - monster.height
        return (x,y)
    
    def blit_all_monster(self):
        """Blit tout les monstres sur le canva des monstres"""
        self.canva_monster.fill((0,0,0,0)) #Remet à 0 le canva

        for pos in self.list_monster :
            for id_monster in self.list_monster[pos] :
                #print("monster")
                self.blit_monster(self.list_monster[pos][id_monster])