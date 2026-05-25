from shared.constants import world
from client.domain.mob.player.player import Player_you,Player_not_you
import pygame,math

class Player_all :
    '''
    Classe de test pour le perso de base
    '''
    def __init__(self,cell_size,screenSize):
        self.dic_players = {}
        self.cell_size = cell_size
        self.client_id = None
        self.spawn_point = world.SPAWN_POINT
        self.me = None
        self.screen_size = screenSize
        self.light = pygame.Surface((screenSize[0],screenSize[1]), pygame.SRCALPHA)
        self.vision = world.NBR_CELL_CAN_SEE//1.2
        self.can_see_others = world.START_SEE

        # Dans __init__ ou à la création de la lanterne :
        self.light_surface_cache = {}

    def get_light_surface(self, radius):
        if radius not in self.light_surface_cache:
            self.light_surface_cache[radius] = self.generate_light_surface(radius)
        return self.light_surface_cache[radius]

    #def create_light(self,screen,projectiles_lumiere,x,y,pos_player,max_blit):
    #    """Permet de faire genre que le personnage voit à une certaine portée"""
    #    self.light.fill((0,0,0))
#
    #    for i in range(0,11,5):
#
    #        for player in self.dic_players.values() :
#
    #            if player == self.me or self.can_see_others :
    #            
    #                if self.distance(pos_player,player) < max_blit+self.vision*self.cell_size :
#
    #                    dx,dy = player.pos_blit[0] + player.animation.height//2,player.pos_blit[1]+player.animation.width//2
#
    #                    self.draw_circle(self.light,(0,0,0,200 - (i)*20),(dx,dy),(self.vision-i/2)*self.cell_size)
#
    #    for proj in projectiles_lumiere.values() :
    #        dx,dy = proj.pos_blit_x + proj.height//2*self.cell_size ,proj.pos_blit_y+proj.width//2*self.cell_size 
    #        #print(x,y,dx,dy)
    #        #print("Player",self.me.pos_blit[0] + player.animation.height//2,self.me.pos_blit[1]+player.animation.width//2)
    #        self.draw_circle(self.light,(0,0,0,200 - (10)*20),(dx,dy),(self.vision-10/4)*self.cell_size)
#
    #    screen.blit(self.light,(0,0))

    def create_light(self, screen, projectiles_lumiere, x, y, pos_player, max_blit):
        self.light.fill((0, 0, 0,255))  # tout noir opaque

        # Joueurs
        for player in self.dic_players.values():
            if player == self.me or self.can_see_others:
                if self.distance(pos_player, player) < max_blit + self.vision * self.cell_size:
                    dx = player.pos_blit[0] + player.animation.height // 2
                    dy = player.pos_blit[1] + player.animation.width // 2
                    radius = int(self.vision)
                    light_surf = self.get_light_surface(radius)

                    self.light.blit(light_surf, (dx - radius, dy - radius),
                                    special_flags=pygame.BLEND_RGBA_SUB)

        # Projectiles lumière
        for proj in projectiles_lumiere.values():
            dx = int(proj.pos_blit_x + proj.height // 2 * self.cell_size)
            dy = int(proj.pos_blit_y + proj.width // 2 * self.cell_size)
            radius = int((self.vision - 10 / 4))
            light_surf = self.get_light_surface(radius)

            self.light.blit(light_surf, (dx - radius, dy - radius),
                            special_flags=pygame.BLEND_RGBA_SUB)

        screen.blit(self.light, (0, 0))

    def generate_light_surface(self, radius):
        size = radius * 2
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))  # transparent par défaut

        for i in range(radius, 0, -20):
            # Centre = alpha 0 (transparent = lumière), bord = alpha 255 (noir = obscurité)
            alpha = int(255 * (1 - i / radius))
            pygame.draw.circle(surface, (0, 0, 0, alpha), (radius, radius), i)

        return surface

    def now_can_see_others(self):

        if not self.can_see_others :
            self.vision = world.NBR_CELL_CAN_SEE
            self.can_see_others = True

    def draw_circle(self,screen,color,pos,r,width=0):
        pygame.draw.circle(screen, color, pos, r, width)

    def add_Player(self,id, is_you = False, pseudo = "Coming soon"):

        if is_you == 1:
            self.dic_players[id] = Player_you(self.cell_size,self.spawn_point,self.screen_size,pseudo,True)
            self.client_id = id
            self.me = self.dic_players[id]

        else :
            self.dic_players[id] = Player_not_you(self.cell_size,self.spawn_point,pseudo,False)

        print("players : ",self.dic_players)

    def blit_client_utils(self,screen,screen_size):

        self.me.draw_utils(screen,screen_size)

    def blit_infos(self,screen,screen_size,mouse_pos):

        self.me.weapons.draw_spells(screen,screen_size,mouse_pos)

    def return_pos(self):
        return self.me.pos_x,self.me.pos_y

    def blit_players(self,screen_global,xscreen,yscreen,pos_player,max_blit,dt):

        for player in self.dic_players.values():

            if not player.is_you :

                if self.distance(pos_player,player) < max_blit :

                    player.draw(screen_global,dt,xscreen,yscreen)

        self.me.draw(screen_global,dt,xscreen,yscreen)

    def draw_light(self,screen_global,projectiles_lumiere,x,y,pos_player,max_blit):

        self.create_light(screen_global,projectiles_lumiere,x,y,pos_player,max_blit)

    def mouse_button_down(self,mouse_pos):

        return self.me.weapons.touch_spells(mouse_pos)
    
    def distance(self,pos_player,pnj):

        dist = (pos_player[0]-pnj.pos_x)**2 + (pos_player[1]-pnj.pos_y)**2
        return math.sqrt(dist)