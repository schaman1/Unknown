import pygame

class Player_all :
    '''
    Classe de test pour le perso de base
    '''
    def __init__(self,canva_size,cell_size):
        self.dic_players = {}
        self.cell_size = cell_size
        self.client_id = None

    def add_Player(self,id,Img_perso = None,pos = (500,500), is_you = False, pseudo = "Coming soon"):
        self.dic_players[id] = Player(Img_perso,self.cell_size,pos[0],pos[1],pseudo,is_you)

        if is_you :
            self.client_id = id

    def draw_players(self,screen_global,center):

        for player in self.dic_players.values():

            if player.is_you :

                screen_global.blit(player.frame_perso[player.frame%4],center)
                player.update_frame()

            else :
                screen_global.blit(player.frame_perso[1],center)
                player.draw(screen_global)

class Player :

    def __init__(self,Img_perso,cell_size,pos_x = 500, pos_y=500, pseudo = "Coming soon",is_you = False):
        self.pos_x = 200#pos_x
        self.pos_y = 200#pos_y
        self.cell_size = cell_size
        self.pseudo = pseudo
        Img = pygame.image.load(Img_perso).convert_alpha() #convert_alpha() pour le fond vide
        self.Img_perso= pygame.transform.scale(Img,(10*cell_size,10*cell_size))
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

    def draw(self,screen):

        screen.blit(self.frame_perso[self.frame%4],self.calculate_pos(self.pos_x,self.pos_y))

        self.update_frame()

    def calculate_pos(self,x,y):
        return (x*self.cell_size,y*self.cell_size)

    def move(self,delta):
        self.pos_x += delta[0]
        self.pos_y += delta[1]

