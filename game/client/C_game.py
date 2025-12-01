import pygame
from client.Personnages_client.player import Player_all
from client.Monster_client.C_monster_all import Monster_all
import var

class Game :
    """Class utilise quand lance le jeu / Permet d'afficher le jeu en gros et devra mettre plus tard les persos à afficher"""
    def __init__(self, cell_size,canva_size):
        self.canva_size = canva_size
        self.cell_size = cell_size
        self.center = (self.canva_size[0]//2,self.canva_size[1]//2)
        self.canva = pygame.Surface((canva_size[0]*cell_size,canva_size[1]*cell_size), pygame.SRCALPHA)
        #self.canva_map = self.map.canva
        self.bg = pygame.image.load("assets/bgGlobal.png").convert()
        self.bg = pygame.transform.scale(self.bg, (canva_size[0],canva_size[1]))
        self.light = pygame.Surface((canva_size[0],canva_size[1]), pygame.SRCALPHA)
        self.create_light(vision = var.NBR_CELL_CAN_SEE)



        # pré-calcul des rects pour chaque cellule
        self.rect_grid = [
            [pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
             for x in range(var.BG_SIZE_SERVER[0])]
            for y in range(var.BG_SIZE_SERVER[1])
        ]

        self.monsters = Monster_all(cell_size,canva_size)

        self.player_all = Player_all(canva_size,cell_size)
        #self.player_all.add_Player("Coming soon",
        #                       Img_perso = "assets/playerImg.png",
        #                       pos = (500,500))

    def update_canva(self,l):
        """Reçoit les données l du serveur et appelle update"""
        for e in l :
            self.switch_cell(e)

    def update_monster(self,data_monster):
        """Reçoit les données des monstres du serv et les envoie à Monster_all"""

        for chunk,list_monster in data_monster.items() :

            for monster in list_monster :

                self.monsters.list_monster[chunk][monster[0]].pos_x = monster[1]
                self.monsters.list_monster[chunk][monster[0]].pos_y = monster[2]

    def create_light(self,vision:int = 10 ):
        """Permet de faire genre que le personnage voit à une certaine portée"""
        self.light.fill((0,0,0))

        for i in range(10):
            pygame.draw.circle(self.light, (0,0,0,200 - (i+1)*20), self.center, (vision+2-i/5)*self.cell_size, width=0)

    def switch_cell(self,el:tuple):
        """Chaque donné contient le x/y et les couleurs = dessine sur le canva !IMPORTANT : dessine pas sur le screen"""

        x,y,r,g,b,a = el
        color = (r,g,b,a)

        self.canva.fill((0,255,0,255), pygame.Rect(500,500,50,50))
        self.canva.fill(color, self.rect_grid[y][x])

    def blit_monster(self,screen,x,y):
        self.monsters.blit_all_monster()
        screen.blit(self.monsters.canva_monster,(x,y))

    def blit_players(self,screen,x,y):
        self.player_all.draw_players()
        screen.blit(self.player_all.screen_Player,(x,y))

    def draw(self,screen,x,y):
        screen.blit(self.bg,(0,0))
        screen.blit(self.canva, (x, y))

        self.blit_monster(screen,x,y)

        screen.blit(self.light,(0,0))

        self.blit_players(screen,x,y)
