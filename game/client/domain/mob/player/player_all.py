from shared.constants import world
from client.domain.mob.player.player import Player_you,Player_not_you
import pygame

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
        self.light = pygame.Surface((screenSize[0],screenSize[1]), pygame.SRCALPHA)
        self.vision = world.NBR_CELL_CAN_SEE

    def create_light(self,screen):
        """Permet de faire genre que le personnage voit à une certaine portée"""
        self.light.fill((0,0,0))

        for i in range(10):

            for player in self.dic_players.values() :

                x,y = player.pos_blit[0] + player.height//1,player.pos_blit[1]+player.width//1

                self.draw_circle(self.light,(0,0,0,200 - (i+1)*20),(x,y),(self.vision-i/2)*self.cell_size)

        screen.blit(self.light,(0,0))

    def draw_circle(self,screen,color,pos,r,width=0):
        pygame.draw.circle(screen, color, pos, r, width)

    def add_Player(self,id, is_you = False, pseudo = "Coming soon"):

        if is_you == 1:
            self.dic_players[id] = Player_you(self.cell_size,self.spawn_point,pseudo,True)
            self.client_id = id
            self.me = self.dic_players[id]

        else :
            self.dic_players[id] = Player_not_you(self.cell_size,self.spawn_point,pseudo,False)

    def blit_client_utils(self,screen,screen_size):

        self.dic_players[self.client_id].draw_utils(screen,screen_size)

    def blit_infos(self,screen,screen_size):

        self.dic_players[self.client_id].weapons.draw_spells(screen,screen_size)

    def return_pos(self):
        return self.dic_players[self.client_id].pos_x,self.dic_players[self.client_id].pos_y

    def blit_players(self,screen_global,center,xscreen,yscreen, mouse_pos):

        for player in self.dic_players.values():

            player.update_pos_blit(xscreen,yscreen)

            if player.is_you :

                player.draw(screen_global,xscreen,yscreen, mouse_pos,center)

            else :

                player.draw(screen_global)

        self.create_light(screen_global)

    def mouse_button_down(self,mouse_pos):

        return self.dic_players[self.client_id].weapons.touch_spells(mouse_pos)