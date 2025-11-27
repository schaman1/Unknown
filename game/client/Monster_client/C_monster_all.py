import pygame

class Monster_all :

    def __init__(self,cell_size,canva_size):

        self.list_monster = None #Liste des monstres dans la map
        self.cell_size = cell_size
        self.canva_monster = pygame.Surface((canva_size[0]*cell_size,canva_size[1]*cell_size), pygame.SRCALPHA)

    def init_monster(self,l):
        """Initialise les monstres reçus du serv"""
        self.list_monster = l
        #print(l)

        for monstre in l :
            #monstre[0] = pygame.image.load(f"assets/monsters/{monstre[0]}.png").convert_alpha()
            monstre[0] = pygame.image.load("assets/playerImg.png").convert_alpha()
            self.canva_monster.blit(monstre[0], (monstre[1]*self.cell_size, monstre[2]*self.cell_size))