import pygame
import pygame.surfarray as surfarray
import struct

from client.domain.mob.player.player import Player_all
from client.domain.mob.monster.monster_all import Monster_all
#import client.OptiClient as njClient
import var

class Game :
    """Class utilise quand lance le jeu / Permet d'afficher le jeu en gros et devra mettre plus tard les persos à afficher"""
    def __init__(self, cell_size):
        self.canva_size = var.BG_SIZE_SERVER
        self.base_movement = var.RATIO

        self.cell_size = cell_size
        self.center = (self.canva_size[0]//2,self.canva_size[1]//2)
        self.canva = pygame.Surface((self.canva_size[0]*cell_size,self.canva_size[1]*cell_size), pygame.SRCALPHA)
        #self.canva.set_colorkey((0,0,0))
        #self.canva_map = self.map.canva
        self.bg = pygame.image.load(var.BG_GLOBAL).convert()
        self.bg = pygame.transform.scale(self.bg, (self.canva_size[0],self.canva_size[1]))
        
        self.light = pygame.Surface((self.canva_size[0],self.canva_size[1]), pygame.SRCALPHA)
        self.create_light(vision = var.NBR_CELL_CAN_SEE)

        # pré-calcul des rects pour chaque cellule
        self.rect_grid = [
            #[pygame.Rect(x * 1, y * 1, 1, 1) #Pour voir toute la map se dessiner
            [pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
             for x in range(var.BG_SIZE_SERVER[0])]
            for y in range(var.BG_SIZE_SERVER[1])
        ]

        self.monsters = Monster_all(cell_size,self.canva_size)

        self.player_all = Player_all(self.canva_size,cell_size)


        self.draw_map = False
        #self.player_all.add_Player("Coming soon",
        #                       Img_perso = "assets/playerImg.png",
        #                       pos = (500,500))

    def update_canva(self,data):
        """Reçoit les données l du serveur et appelle update"""

        rgb = surfarray.pixels3d(self.canva)
        alpha = surfarray.pixels_alpha(self.canva)

        for x, y, r, g, b, a in struct.iter_unpack("!hhBBBB", data[3:]):
            px = x * self.cell_size
            py = y * self.cell_size
            rgb[px:px+self.cell_size, py:py+self.cell_size] = (r, g, b)
            alpha[px:px+self.cell_size, py:py+self.cell_size] = a

        del rgb, alpha

    def update_monster(self,data_monster):
        """Reçoit les données des monstres du serv et les envoie à Monster_all"""

        for (chunk, id, x, y) in data_monster :
                
            self.monsters.dic_monster[chunk][id].pos_x = x
            self.monsters.dic_monster[chunk][id].pos_y = y

    def create_light(self,vision:int = 10 ):
        """Permet de faire genre que le personnage voit à une certaine portée"""
        self.light.fill((0,0,0))

        for i in range(10):
            pygame.draw.circle(self.light, (0,0,0,200 - (i+1)*20), self.center, (vision+2-i/5)*self.cell_size, width=0)


    def blit_monster(self,screen,x,y):
        self.monsters.blit_all_monster(screen,x,y)
        #screen.blit(self.monsters.canva_monster,(x,y))

    def blit_players(self,screen,x,y):
        self.player_all.draw_players(screen,self.center,x,y)
        #screen.blit(self.player_all.screen_Player,(x,y))

    def draw(self,screen,x,y):
        """Blit le canva sur le screen à la position x,y"""

        screen.blit(self.bg,(0,0))
        screen.blit(self.canva, (x, y))
        #screen.blit(self.canva,(0,0)) #Pour voir la map en entier

        self.blit_monster(screen,x,y)
        self.blit_players(screen,x,y)

        #screen.blit(self.light,(0,0))
        
        if self.draw_map :
            screen.fill((0,0,0))


    def convert_from_base(self,nbr):
        return nbr//self.base_movement