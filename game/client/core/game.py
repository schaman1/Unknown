import pygame

from client.domain.mob.player.player_all import Player_all
from client.domain.mob.monster.monster_all import Monster_all
from client.domain.projectile.projectile_manager import ProjectileManager
from client.domain.actions.mini_map import MiniMap
from client.domain.actions.map import Map

from client.config import assets
from shared.constants import world

class Game :
    """Class utilise quand lance le jeu / Permet d'afficher le jeu en gros et devra mettre plus tard les persos à afficher"""
    def __init__(self, cell_size, screenSize):
        self.canva_size = world.BG_SIZE_SERVER
        self.base_movement = world.RATIO

        self.cell_size = cell_size
        self.screen_size = screenSize
        self.center = (screenSize[0]//2,screenSize[1]//2)
        
        #self.canva = pygame.Surface((self.canva_size[0]*cell_size,self.canva_size[1]*cell_size), pygame.SRCALPHA)
        self.canva = Map(screenSize,cell_size)
        
        self.bg = pygame.image.load(assets.BG_GLOBAL).convert()
        self.bg = pygame.transform.scale(self.bg, (self.canva_size[0],self.canva_size[1]))

        self.light = pygame.Surface((self.canva_size[0],self.canva_size[1]), pygame.SRCALPHA)
        self.create_light(vision = world.NBR_CELL_CAN_SEE)

        self.monsters = Monster_all(cell_size)

        self.player_all = Player_all(cell_size)

        self.mini_map = MiniMap(world.NBR_CELL_CAN_SEE,assets.MAP_SEEN,assets.MAP_UNSEEN,self.canva_size,self.cell_size)

        self.projectiles = ProjectileManager(cell_size)

        self.player_command = []
        self.blit_info=False
        self.spell_blit_mouse=None
        
    def draw_intro_start(self,screen):

        screen.blit(pygame.image.load(assets.BG_WAITING).convert(),(0,0))

    def draw_intro_end(self,screen):

        screen.blit(pygame.image.load(assets.BG_WAITING).convert(),(0,0)) #Faire un decrescendo ou un truc stylé d'animation

        return True #If end animation else return False

    #def update_canva(self,data):
    #    """Reçoit les données l du serveur et appelle update"""
#
    #    rgb = surfarray.pixels3d(self.canva)
    #    alpha = surfarray.pixels_alpha(self.canva)
#
    #    for x, y, r, g, b, a in struct.iter_unpack("!hhBBBB", data[3:]):
    #        px = x * self.cell_size
    #        py = y * self.cell_size
    #        rgb[px:px+self.cell_size, py:py+self.cell_size] = (r, g, b)
    #        alpha[px:px+self.cell_size, py:py+self.cell_size] = a
#
    #    del rgb, alpha

    def update_monster(self,data_monster):
        """Reçoit les données des monstres du serv et les envoie à Monster_all"""

        for (chunk, id, x, y) in data_monster :
                
            self.monsters.dic_monster[chunk][id].pos_x = x
            self.monsters.dic_monster[chunk][id].pos_y = y

    def create_light(self,vision):
        """Permet de faire genre que le personnage voit à une certaine portée"""
        self.light.fill((0,0,0))

        for i in range(10):
            self.draw_circle(self.light,(0,0,0,200 - (i+1)*20),self.center,(vision-i/2)*self.cell_size)

    def shot(self):
        if not self.blit_info:
            self.player_command.append(self.player_all.me.shot())

    def draw_circle(self,screen,color,pos,r,width=0):
        pygame.draw.circle(screen, color, pos, r, width)

    def blit_monsters(self,screen,x,y):
        self.monsters.blit_all_monsters(screen,x,y)

    def blit_players(self,screen,x,y,mouse_pos):
        self.player_all.blit_players(screen,self.center,x,y,mouse_pos)

    def blit_projectiles_explosions(self,screen,x,y,dt):

        self.projectiles.blit_projectiles_explosions(screen,x,y,dt)

    def blit_utils(self,screen,screen_size):

        self.player_all.blit_client_utils(screen,screen_size)

    def blit_infos(self,screen,screen_size,mouse_pos):

        if self.blit_info :

            screen.fill((50,50,50)) #A changer pour mettre transparence

            self.player_all.blit_infos(screen,screen_size)

            if self.spell_blit_mouse!=None:
                screen.blit(self.spell_blit_mouse,mouse_pos)

    def draw(self,screen,x,y,dt,mouse_pos=None):
        """Blit le canva sur le screen à la position x,y"""

        #x,y = 0,0  #Pour voir toute la map

        screen.blit(self.bg,(0,0))
        #screen.fill((0,0,0))

        self.canva.draw_map(x,y,self.player_all.return_pos(),screen)

        self.blit_monsters(screen,x,y)
        self.blit_players(screen,x,y, mouse_pos)
        self.blit_projectiles_explosions(screen,x,y,dt)

        screen.blit(self.light,(0,0))

        self.blit_utils(screen,self.screen_size)

        pos = self.player_all.return_pos()
        pos = (self.convert_from_base(pos[0]),self.convert_from_base(pos[1]))

        self.mini_map.draw_map(screen,pos)
        self.blit_infos(screen,self.screen_size,mouse_pos)

    def convert_from_base(self,nbr): #Est utilisé ???
        return nbr//self.base_movement
    
    def create_projectile(self,id,pos_x,pos_y,angle,vitesse,weight,id_img):

        self.projectiles.create_projectile(id,pos_x,pos_y,angle,vitesse,weight,id_img)

    def update_next_allowed_shot(self,delta_time):

        self.player_all.me.weapons.update_next_allowed_shot(delta_time)

    def trigger_mouse_down(self,mouse_pos):

        if self.blit_info :

            info,spell_1,spell_2 =  self.player_all.mouse_button_down(mouse_pos)

            if info==1:
                self.spell_blit_mouse = None

            elif info==0: #Blit spell_1 a pos=souris car c l'img du spell
                self.spell_blit_mouse =spell_1 

            return info,spell_1,spell_2
        
        else :

            return -1,None,None
        
    def trigger_info_key(self):

        if self.blit_info and self.spell_blit_mouse != None:
            
            self.player_all.me.weapons.stop_holding_spell()
            self.spell_blit_mouse=None

        self.blit_info = not self.blit_info
