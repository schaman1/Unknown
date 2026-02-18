import pygame,time
from client.config import assets,weapon
from shared.constants import world

class DefaultExplosion:

    def __init__(self,pos,projectile,cell_size):

        self.pos = pos
        self.time_remaining = None
        self.base_movement = world.RATIO
        self.cell_size = cell_size
        self.frame = 0

        self.imgs = self.load(projectile)

    def die(self):
        if time.perf_counter() > self.time_remaining :
            return True
        
        else :
            return False

    def load(self,projectile):
        """No more use bcs keep the same img as the projectile but if we want to changer we will have to use this again"""

        Imgs = []

        if projectile.id_img == 1 :

            self.time_remaining = 0.3+time.perf_counter()

            for i in range(4):
                self.width,self.height = weapon.PROJECTILE_2_WIDTH,weapon.PROJECTILE_2_HEIGHT
                img = pygame.image.load(assets.SPELLS[projectile.id_img]).convert_alpha() #convert_alpha() pour le fond vide
                img = pygame.transform.scale(img,(self.width*self.cell_size,self.height*self.cell_size)) 
                rotated_img = pygame.transform.rotate(img, projectile.angle)
                Imgs.append(rotated_img)

        elif projectile.id_img==0:

            self.time_remaining = 0.3+time.perf_counter()

            for i in range(4):
                self.width,self.height = weapon.PROJECTILE_0_WIDTH,weapon.PROJECTILE_2_HEIGHT
                img = pygame.image.load(assets.PROJECTILE_0[i]).convert_alpha() #convert_alpha() pour le fond vide
                img = pygame.transform.scale(img,(self.width*self.cell_size,self.height*self.cell_size)) 
                rotated_img = pygame.transform.rotate(img, projectile.angle)
                Imgs.append(rotated_img)

        elif projectile.id_img >=3:

            self.time_remaining=0.2+time.perf_counter()

            self.width,self.height = projectile.width,projectile.height
            Imgs = projectile.imgs
        
        else :
            print("Unknown weapon id in client for explosion, id : ",projectile.id_img)

        return Imgs

    def blit(self,screen,xscreen,yscreen):

        rect_center = self.calculate_pos_blit(xscreen,yscreen)
        screen.blit(self.imgs[0],rect_center)

        self.update_frame()

    def update_frame(self):
        self.frame = (self.frame+1)%200

    def calculate_pos_blit(self,x,y):

        xs = self.convert_from_base(self.pos[0]*self.cell_size) +x
        ys = self.convert_from_base((self.pos[1]) * self.cell_size) +y #Regle un petit soucis
        rect = self.imgs[self.frame//50].get_rect(center=(xs, ys))
        return rect
    
    def convert_from_base(self,nbr):
        return nbr//self.base_movement