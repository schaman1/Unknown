from shared.constants import world
from client.domain.mob.player.player import Player

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
        self.dic_players[id] = Player(self.cell_size,self.spawn_point,pseudo,is_you)

        if is_you :
            self.client_id = id

    def return_pos(self):
        return self.dic_players[self.client_id].pos_x,self.dic_players[self.client_id].pos_y

    def blit_players(self,screen_global,center,xscreen,yscreen, mouse_pos):

        for player in self.dic_players.values():

            if player.is_you :

                #screen_global.blit(player.frame_perso[player.frame%4],center)
                player.draw(screen_global,xscreen,yscreen, mouse_pos,center)
                #player.update_frame()

            else :
                #screen_global.blit(player.frame_perso[1],(player.pos_x,player.pos_y))
                player.draw(screen_global,xscreen,yscreen)