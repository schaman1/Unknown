from client.config import assets,weapon
from shared.constants import world
import pygame,math

class DefaultProjectile :

    def __init__(self,pos_x,pos_y,angle,vitesse,weight,id_img,cell_size):

        self.pos_x,self.pos_y = pos_x,pos_y
        self.cell_size = cell_size
        self.angle = angle
        self.id_img = id_img

        self.height,self.width = None,None
        self.base_movement = world.RATIO
        self.weight = 255*self.base_movement

        self.vx,self.vy = self.create_vx_vy(angle,vitesse)

        self.imgs = self.create_img(id_img,cell_size,angle)
        self.frame = 0

    def create_vx_vy(self,angle,vitesse):
        rad = math.radians(angle)
        vx = int(math.cos(rad)*vitesse)
        vy = -int(math.sin(rad)*vitesse)
        return vx,vy
    
    def gravity(self,dt):
        pass#self.vy+=self.weight*dt
    
    def move(self,dt):

        self.gravity(dt)

        self.pos_x+=self.vx*dt#int(1000*dt)#
        self.pos_y+=self.vy*dt#1000*dt#

    def create_img(self,id_img,cell_size,angle):

        Imgs = []

        if id_img==3:
            self.width,self.height = weapon.PROJECTILE_3_WIDTH,weapon.PROJECTILE_3_HEIGHT
            img = pygame.image.load(assets.SPELLS[id_img]).convert_alpha() #convert_alpha() pour le fond vide
            img = pygame.transform.scale(img,(self.width*cell_size,self.height*cell_size)) 
            rotated_img = pygame.transform.rotate(img, angle)
            Imgs.append(rotated_img)

        elif id_img == 1 :
            for i in range(4):
                self.width,self.height = weapon.PROJECTILE_2_WIDTH,weapon.PROJECTILE_2_HEIGHT
                img = pygame.image.load(assets.SPELLS[id_img]).convert_alpha() #convert_alpha() pour le fond vide
                img = pygame.transform.scale(img,(self.width*cell_size,self.height*cell_size)) 
                rotated_img = pygame.transform.rotate(img, angle)
                Imgs.append(rotated_img)

        elif id_img == 0 :
            for i in range(4):
                self.width,self.height = weapon.PROJECTILE_0_WIDTH,weapon.PROJECTILE_0_HEIGHT
                img = pygame.image.load(assets.PROJECTILE_0[i]).convert_alpha() #convert_alpha() pour le fond vide
                img = pygame.transform.scale(img,(self.width*cell_size,self.height*cell_size)) 
                rotated_img = pygame.transform.rotate(img, angle)
                Imgs.append(rotated_img)

        else :
            print("Unknown weapon id in client")

        return Imgs
        
    def blit(self,screen,xscreen,yscreen):

        #self.pos_x,self.pos_y = 63305, 16125

        rect_center = self.calculate_pos_blit(xscreen,yscreen)
        screen.blit(self.imgs[self.frame//50],rect_center)

        self.update_frame()

    def update_frame(self):
        self.frame = (self.frame+1)%1

    def calculate_pos_blit(self,x,y):
        xs = self.convert_from_base(self.pos_x*self.cell_size) +x
        ys = self.convert_from_base((self.pos_y) * self.cell_size) +y #Regle un petit soucis
        rect = self.imgs[self.frame//50].get_rect(center=(xs, ys))
        return rect
    
    def convert_from_base(self,nbr):
        return nbr//self.base_movement