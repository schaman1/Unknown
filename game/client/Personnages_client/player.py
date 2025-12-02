import pygame

class Player_all :
    '''
    Classe de test pour le perso de base
    '''
    def __init__(self,canva_size,cell_size):
        self.dic_players = {}
        self.cell_size = cell_size
        self.screen_Player = pygame.Surface((canva_size[0]*cell_size,canva_size[1]*cell_size), pygame.SRCALPHA)
        self.client_id = None

    def add_Player(self,id,Img_perso = None,pos = (500,500), is_you = False, pseudo = "Coming soon"):
        self.dic_players[id] = Player(Img_perso,self.cell_size,pos[0],pos[1],pseudo,is_you)

        if is_you :
            self.client_id = id

    def draw_players(self,screen_global,center):

        self.screen_Player.fill((0,0,0,0))
        for player in self.dic_players.values():

            if player.is_you :

                screen_global.blit(player.Img_perso,center)

            else :

                player.draw(self.screen_Player)

class Player :

    def __init__(self,Img_perso,cell_size,pos_x = 500, pos_y=500, pseudo = "Coming soon",is_you = False):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.cell_size = cell_size
        self.pseudo = pseudo
        Img = pygame.image.load(Img_perso).convert() #convert_alpha() pour le fond vide
        self.Img_perso= pygame.transform.scale(Img,(10*cell_size,10*cell_size))
        self.is_you = is_you

    def draw(self,screen):
        screen.blit(self.Img_perso,self.calculate_pos(self.pos_x,self.pos_y))

    def calculate_pos(self,x,y):
        return (x*self.cell_size,y*self.cell_size)

    def move(self,delta):
        self.pos_x += delta[0]
        self.pos_y += delta[1]

