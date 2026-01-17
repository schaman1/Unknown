import pygame
import pygame.surfarray as surfarray
import struct

from client.domain.mob.player.player_all import Player_all
from client.domain.mob.monster.monster_all import Monster_all
from client.domain.projectile.projectile_manager import ProjectileManager
from client.domain.weapon.weapon_manager import WeaponManager
from client.domain.actions.map import Map

from client.config import assets
from shared.constants import world

class Game :
    """Class utilise quand lance le jeu / Permet d'afficher le jeu en gros et devra mettre plus tard les persos à afficher"""
    def __init__(self, cell_size, screenSize):
        self.canva_size = world.BG_SIZE_SERVER
        self.base_movement = world.RATIO

        self.cell_size = cell_size
        self.center = (screenSize[0]//2,screenSize[1]//2)
        self.canva = pygame.Surface((self.canva_size[0]*cell_size,self.canva_size[1]*cell_size), pygame.SRCALPHA)
        self.bg = pygame.image.load(assets.BG_GLOBAL).convert()
        self.bg = pygame.transform.scale(self.bg, (self.canva_size[0],self.canva_size[1]))

        self.light = pygame.Surface((self.canva_size[0],self.canva_size[1]), pygame.SRCALPHA)
        self.create_light(vision = world.NBR_CELL_CAN_SEE)

        # pré-calcul des rects pour chaque cellule
        self.rect_grid = [
            #[pygame.Rect(x * 1, y * 1, 1, 1) #Pour voir toute la map se dessiner
            [pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
             for x in range(self.canva_size[0])]
            for y in range(self.canva_size[1])
        ]

        self.monsters = Monster_all(cell_size,self.canva_size)

        self.player_all = Player_all(cell_size)

        self.map = Map(world.NBR_CELL_CAN_SEE,assets.MAP_SEEN,assets.MAP_UNSEEN,self.canva_size,self.cell_size)

        self.projectiles = ProjectileManager(self.cell_size)

        self.weapons = WeaponManager()

        #self.player_all.add_Player("Coming soon",
        #                       Img_perso = "assets/playerImg.png",
        #                       pos = (500,500))

    def draw_intro_start(self,screen):

        screen.blit(pygame.image.load(assets.BG_WAITING).convert(),(0,0))

    def draw_intro_end(self,screen):

        screen.blit(pygame.image.load(assets.BG_WAITING).convert(),(0,0)) #Faire un decrescendo ou un truc stylé d'animation

        return True #If end animation else return False

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

    def create_light(self,vision):
        """Permet de faire genre que le personnage voit à une certaine portée"""
        self.light.fill((0,0,0))

        for i in range(10):
            self.draw_circle(self.light,(0,0,0,200 - (i+1)*20),self.center,(vision-i/5)*self.cell_size)

    def draw_circle(self,screen,color,pos,r,width=0):
        pygame.draw.circle(screen, color, pos, r, width)

    def blit_monsters(self,screen,x,y):
        self.monsters.blit_all_monsters(screen,x,y)

    def blit_players(self,screen,x,y,mouse_pos):
        self.player_all.blit_players(screen,self.center,x,y,mouse_pos)

    def blit_projectiles(self,screen,x,y,dt):

        self.projectiles.blit_projectiles(screen,x,y,dt)

    def draw(self,screen,x,y,dt,mouse_pos=None):
        """Blit le canva sur le screen à la position x,y"""

        #x,y = 0,0  #Pour voir toute la map

        screen.blit(self.bg,(0,0))
        #screen.fill((0,0,0))

        screen.blit(self.canva, (x, y))

        self.blit_monsters(screen,x,y)
        self.blit_players(screen,x,y, mouse_pos)
        self.weapons.draw_weapon(screen,mouse_pos,self.center)
        self.blit_projectiles(screen,x,y,dt)

        #screen.blit(self.light,(0,0))
        pos = self.player_all.return_pos()
        pos = (self.convert_from_base(pos[0]),self.convert_from_base(pos[1]))
        self.map.draw_map(screen,pos)
        
    def convert_from_base(self,nbr): #Est utilisé ???
        return nbr//self.base_movement