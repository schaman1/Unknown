import pygame
from client.C_mob import Mob

class Skeleton(Mob) :

    def __init__(self, x,y,pos_chunk,cell_size):

        super().__init__(x,y,cell_size,size=(5,5))

        self.name = "Skeleton"
        self.chunk = pos_chunk
        self.frame_perso = []
        self.frame = 0
        #self.width ,self.height = self.Img.get_size() #Get la taille de l'img
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

    def blit(self,screen,x,y):
        screen.blit(self.frame_perso[self.frame%4],self.calculate_pos_blit(x,y))
        self.update_frame()