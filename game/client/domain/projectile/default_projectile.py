from client.config import assets
from shared.constants import size_display,world
import pygame

class DefaultProjectile :

    def __init__(self,pos_x,pos_y,angle,vitesse,id_img,cell_size):

        self.pos_x,self.pos_y = pos_x,pos_y
        self.cell_size = cell_size

        self.height,self.width = size_display.PIOCHE_SIZE_HEIGHT,size_display.PIOCHE_SIZE_WIDTH
        self.base_movement = world.RATIO

        self.vx,self.vy = self.create_vx_vy(angle,vitesse)

        self.img = self.create_img(id_img,cell_size)

    def create_vx_vy(self,angle,vitesse):

        return 0,0
    
    def move(self,dt):

        self.pos_x+=self.vx*dt
        self.pos_y+=self.vy*dt

    def create_img(self,id_img,cell_size):

        if id_img == 0 :
            Img = pygame.image.load(assets.PIOCHE).convert_alpha() #convert_alpha() pour le fond vide
            return pygame.transform.scale(Img,(size_display.PIOCHE_SIZE_WIDTH*cell_size,size_display.PIOCHE_SIZE_HEIGHT*cell_size)) 
        
    def blit(self,screen,xscreen,yscreen):

        pos = self.calculate_pos_blit(xscreen,yscreen)
        screen.blit(self.img,pos)

    def calculate_pos_blit(self,x,y):
        xs = self.convert_from_base(self.pos_x*self.cell_size) - self.width//2*self.cell_size +x
        ys = self.convert_from_base((self.pos_y+1) * self.cell_size) - self.height*self.cell_size +y #Regle un petit soucis
        return (xs,ys)
    
    def convert_from_base(self,nbr):
        return nbr//self.base_movement