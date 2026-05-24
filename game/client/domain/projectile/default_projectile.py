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
        self.weight = weight

        self.vx,self.vy = self.create_vx_vy(angle,vitesse)

        self.imgs = self.create_img(id_img,cell_size,angle)
        self.frame = 0
        self.len_anim = 0.1
        self.current_time = 0

    def create_vx_vy(self,angle,vitesse):
        rad = math.radians(angle)
        vx = int(math.cos(rad)*vitesse)
        vy = -int(math.sin(rad)*vitesse)
        return vx,vy
    
    def gravity(self,dt):

        self.vy += self.base_movement*self.weight*dt

        gravity_power_mult = 1#Diff car dans les game grav plus forte quand tu tombe pour meilleur feeling
        if self.vy < 0:
            gravity_power_mult -=0.1
        else :
            gravity_power_mult += 0.1

        if self.weight != 0:
            self.vy = self.vy*(gravity_power_mult**(dt*60))
    
    def move(self,dt):

        self.gravity(dt)

        self.pos_x+=self.vx*dt#int(1000*dt)#
        self.pos_y+=self.vy*dt#1000*dt#

    def create_img(self,id_img,cell_size,angle):

        Imgs = []

        if id_img==5:
            self.width,self.height = weapon.PROJECTILE_5_WIDTH,weapon.PROJECTILE_5_HEIGHT
            img = pygame.image.load(assets.SPELLS[id_img]).convert_alpha() #convert_alpha() pour le fond vide
            img = pygame.transform.scale(img,(self.width*cell_size,self.height*cell_size)) 
            rotated_img = pygame.transform.rotate(img, angle)
            Imgs.append(rotated_img)

        elif id_img==4:
            self.width,self.height = weapon.PROJECTILE_4_WIDTH,weapon.PROJECTILE_4_HEIGHT
            img = pygame.image.load(assets.SPELLS[id_img]).convert_alpha() #convert_alpha() pour le fond vide
            img = pygame.transform.scale(img,(self.width*cell_size,self.height*cell_size)) 
            rotated_img = pygame.transform.rotate(img, angle)
            Imgs.append(rotated_img)

        elif id_img==3:
            self.width,self.height = weapon.PROJECTILE_3_WIDTH,weapon.PROJECTILE_3_HEIGHT
            img = pygame.image.load(assets.SPELLS[id_img]).convert_alpha() #convert_alpha() pour le fond vide
            img = pygame.transform.scale(img,(self.width*cell_size,self.height*cell_size)) 
            rotated_img = pygame.transform.rotate(img, angle)
            Imgs.append(rotated_img)

        elif id_img == 2:
            for i in range(4):
                self.width,self.height = weapon.PROJECTILE_2_WIDTH,weapon.PROJECTILE_2_HEIGHT
                img = pygame.image.load(assets.SPELLS[id_img]).convert_alpha() #convert_alpha() pour le fond vide
                img = pygame.transform.scale(img,(self.width*cell_size,self.height*cell_size)) 
                rotated_img = pygame.transform.rotate(img, angle)
                Imgs.append(rotated_img)

        elif id_img == 1:
            for i in range(4):
                self.width,self.height = weapon.PROJECTILE_0_WIDTH,weapon.PROJECTILE_0_HEIGHT
                img = pygame.image.load(assets.PROJECTILE_0[i]).convert_alpha() #convert_alpha() pour le fond vide
                img = pygame.transform.scale(img,(self.width*cell_size,self.height*cell_size)) 
                rotated_img = pygame.transform.rotate(img, angle)
                Imgs.append(rotated_img)
            
        elif id_img==7:
            self.width,self.height = weapon.PROJECTILE_7_WIDTH,weapon.PROJECTILE_7_HEIGHT
            img = pygame.image.load(assets.SPELLS[id_img]).convert_alpha() #convert_alpha() pour le fond vide
            img = pygame.transform.scale(img,(self.width*cell_size,self.height*cell_size)) 
            rotated_img = pygame.transform.rotate(img, angle)
            Imgs.append(rotated_img)
            
        elif id_img==8:
            self.width,self.height = weapon.PROJECTILE_8_WIDTH,weapon.PROJECTILE_8_HEIGHT
            img = pygame.image.load(assets.PROJECTILE_8_0).convert_alpha() #convert_alpha() pour le fond vide
            img = pygame.transform.scale(img,(self.width*cell_size,self.height*cell_size)) 
            rotated_img = pygame.transform.rotate(img, angle)
            Imgs.append(rotated_img)

        elif id_img==9:
            self.width,self.height = weapon.PROJECTILE_9_WIDTH,weapon.PROJECTILE_9_HEIGHT #*2 car c pour l'image totale = 4 frame
            img = pygame.image.load(assets.PROJECTILE_9_0).convert_alpha() #convert_alpha() pour le fond vide
            img = pygame.transform.scale(img,(self.width*cell_size*2,self.height*cell_size*2)) 
            #rotated_img = pygame.transform.rotate(img, angle)
            Imgs = self.decoupe_img(img,(self.width*cell_size,self.height*cell_size))

        else :
            print("Unknown weapon id in client /domain/projectile/Default projectiles",id_img)

        return Imgs
        
    def blit(self,screen,xscreen,yscreen,dt):

        #self.pos_x,self.pos_y = 63305, 16125

        rect_center = self.calculate_pos_blit(xscreen,yscreen)
        #screen.blit(self.imgs[self.frame//50],rect_center)
        screen.blit(self.imgs[self.frame],rect_center)

        self.update_frame(dt)

    def update_frame(self,dt):

        self.current_time+=dt
        if self.current_time>=self.len_anim :
            self.current_time-=self.len_anim
            self.frame = (self.frame+1)%len(self.imgs)

    def calculate_pos_blit(self,x,y):
        xs = self.convert_from_base(self.pos_x*self.cell_size) +x
        ys = self.convert_from_base((self.pos_y) * self.cell_size) +y #Regle un petit soucis
        rect = self.imgs[self.frame].get_rect(center=(xs, ys))
        return rect
    
    def convert_from_base(self,nbr):
        return nbr//self.base_movement
    
    def decoupe_img(self,img,size):
        res = []
        for i in range(0,img.get_height(),size[1]):
            for j in range(0,img.get_width(),size[0]):

                rect = pygame.Rect(j,i,size[0],size[1])
                sub_img = img.subsurface(rect).copy()
                #sub_img = p
                res.append(sub_img)

        return res