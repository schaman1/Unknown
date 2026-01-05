import pygame
from client.domain.mob.mob import Mob
from client.config import assets
from shared.constants import world

class Player(Mob) :

    def __init__(self,cell_size,pos, pseudo = "Coming soon",is_you = False):

        super().__init__(pos[0],pos[1],cell_size,size=(world.PLAYER_SIZE_WIDTH,world.PLAYER_SIZE_HEIGHT))

        self.pseudo = pseudo
        self.is_you = is_you
        self.frame_perso = []
        self.frame = 0
        self.frame_multiplier = 0

        self.init_Img(cell_size)

    def init_Img(self,cell_size):
        for i in range(4):
            Img = pygame.image.load(assets.PLAYER_IDLE+f"{i+1}"+".png").convert_alpha() #convert_alpha() pour le fond vide
            Img = pygame.transform.scale(Img,(self.width*cell_size,self.height*cell_size))
            self.frame_perso.append(Img)

    def update_frame(self):
        self.frame_multiplier +=1
        if self.frame_multiplier >= 100 :
            self.frame +=1
            self.frame_multiplier = 0

    def draw(self,screen,xscreen,yscreen):
        
        pos = self.calculate_pos_blit(xscreen,yscreen)
        screen.blit(self.frame_perso[self.frame%4],pos)
        self.update_frame()
        
        pygame.draw.rect( #Pour voir ou le perso est en temps reel
            screen,
            (255, 255, 255),  # couleur (blanc)
            pygame.Rect((self.pos_x*self.cell_size)//100+xscreen, self.pos_y*self.cell_size//100+yscreen, self.cell_size, self.cell_size)
        )

    #def calculate_pos(self,xscreen,yscreen):
    #    return (self.pos_x*self.cell_size+xscreen,self.pos_y*self.cell_size+yscreen)

    def move(self,delta):
        self.pos_x = delta[0]
        self.pos_y = delta[1]
        

