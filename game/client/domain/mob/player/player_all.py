from shared.constants import world
from client.domain.mob.player.player import Player_you,Player_not_you

class Player_all :
    '''
    Classe de test pour le perso de base
    '''
    def __init__(self,cell_size):
        self.dic_players = {}
        self.cell_size = cell_size
        self.client_id = None
        self.spawn_point = world.SPAWN_POINT

    def add_Player(self,id, is_you = False, pseudo = "Coming soon"):

        if is_you == 1:
            self.dic_players[id] = Player_you(self.cell_size,self.spawn_point,pseudo,is_you)
            self.client_id = id

        else :
            self.dic_players[id] = Player_not_you(self.cell_size,self.spawn_point,pseudo,is_you)

    def return_pos(self):
        return self.dic_players[self.client_id].pos_x,self.dic_players[self.client_id].pos_y

    def blit_players(self,screen_global,center,xscreen,yscreen, mouse_pos):

        for player in self.dic_players.values():

            if player.is_you :

                player.draw(screen_global,xscreen,yscreen, mouse_pos,center)

            else :

                player.draw(screen_global,xscreen,yscreen)