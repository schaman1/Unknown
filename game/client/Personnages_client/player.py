import pygame,var
from client.C_mob import Mob


class Player_all :
    '''
    Classe de test pour le perso de base
    '''
    def __init__(self,canva_size,cell_size):
        self.dic_players = {}
        self.cell_size = cell_size
        self.client_id = None
        self.spawn_point = var.SPAWN_POINT

    def add_Player(self,id, is_you = False, pseudo = "Coming soon"):
        self.dic_players[id] = Player(self.cell_size,self.spawn_point,pseudo,is_you)

        if is_you :
            self.client_id = id

    def draw_players(self,screen_global,center,xscreen,yscreen):

        for player in self.dic_players.values():

            if player.is_you :

                #screen_global.blit(player.frame_perso[player.frame%4],center)
                player.draw(screen_global,xscreen,yscreen)
                #player.update_frame()

            else :
                #screen_global.blit(player.frame_perso[1],(player.pos_x,player.pos_y))
                player.draw(screen_global,xscreen,yscreen)

class Player(Mob) :

    def __init__(self,cell_size,pos, pseudo = "Coming soon",is_you = False):

        super().__init__(pos[0],pos[1],cell_size,size=(5,5))

        self.pseudo = pseudo
        self.is_you = is_you
        self.frame_perso = []
        self.frame = 0
        self.frame_multiplier = 0

        self.init_Img(cell_size)

    def init_Img(self,cell_size):
        for i in range(4):
            Img = pygame.image.load(f"assets/player_frame_{i+1}.png").convert_alpha() #convert_alpha() pour le fond vide
            Img = pygame.transform.scale(Img,(10*cell_size,10*cell_size))
            self.frame_perso.append(Img)

    def update_frame(self):
        self.frame_multiplier +=1
        if self.frame_multiplier >= 100 :
            self.frame +=1
            self.frame_multiplier = 0

    def draw(self,screen,xscreen,yscreen):
        
        screen.blit(self.frame_perso[self.frame%4],self.calculate_pos_blit(xscreen,yscreen))
        self.update_frame()

    #def calculate_pos(self,xscreen,yscreen):
    #    return (self.pos_x*self.cell_size+xscreen,self.pos_y*self.cell_size+yscreen)

    def move(self,delta):
        self.pos_x += delta[0]
        self.pos_y += delta[1]
        

