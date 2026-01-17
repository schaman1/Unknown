import pygame, math
from client.domain.mob.mob import Mob
from client.config import assets,weapon
from shared.constants import size_display
from client.domain.weapon.weapon_manager import WeaponManager

class Player_you(Mob) :

    def __init__(self,cell_size,pos, pseudo = "Coming soon",is_you = True):

        super().__init__(pos[0],pos[1],cell_size,size=(size_display.PLAYER_SIZE_WIDTH,size_display.PLAYER_SIZE_HEIGHT))

        self.pseudo = pseudo
        self.is_you = is_you
        self.frame_perso_left = []
        self.frame_perso_right = []
        #self.frame_weapon = []
        self.frame = 0
        self.frame_multiplier = 0

        self.init_Img(cell_size)

        self.weapons = WeaponManager()

    def init_Img(self,cell_size):
        for i in range(4):
            Img = pygame.image.load(assets.PLAYER_IDLE+f"{i+1}"+".png").convert_alpha() #convert_alpha() pour le fond vide
            Img = pygame.transform.scale(Img,(self.width*cell_size,self.height*cell_size))
            Img_flip = pygame.transform.flip(Img, True, False)
            self.frame_perso_right.append(Img)
            self.frame_perso_left.append(Img_flip)
        #self.frame_weapon.append(Img_weapon)

    def update_frame(self):
        self.frame_multiplier +=1
        if self.frame_multiplier >= 100 :
            self.frame +=1
            self.frame_multiplier = 0
    
    def get_angle(self, pos, mouse_pos) -> int:
        '''renvoie l'angle entre le perso et la souris en int'''
        oppose = mouse_pos[1] - pos[1]
        adjacent = mouse_pos[0] - pos[0]
        mouse_angle = int(math.degrees(math.atan2(-oppose,adjacent))) #comme atan() mais en 2D
        return mouse_angle

    def draw(self,screen,xscreen,yscreen, mouse_pos=None,center=None):
        
        pos = self.calculate_pos_blit(xscreen,yscreen)
        self.angle_weapon = self.get_angle(pos, mouse_pos)
        #self.angle = self.get_angle(center, mouse_pos)
        
        perso_right = self.frame_perso_right[self.frame%4]
        perso_left = self.frame_perso_left[self.frame%4]

        if mouse_pos[0] > center[0]: #affiche le perso regardant une dirrection en fonction de la souris
            screen.blit(perso_left,pos)
        else :
            screen.blit(perso_right, pos)

        self.draw_weapon(screen,self.angle_weapon,pos)

        self.update_frame()
        
        pygame.draw.rect( #Pour voir où le perso est en temps reel
            screen,
            (255, 255, 255),  # couleur (blanc)
            pygame.Rect((self.pos_x*self.cell_size)//100+xscreen, self.pos_y*self.cell_size//100+yscreen, self.cell_size, self.cell_size)
        )

    def draw_weapon(self,screen,angle,pos_draw) :

        self.weapons.draw_weapon(screen,angle,pos_draw, self.frame)

    def add_weapon(self,i,id_weapon,loading_time,nbr_spell_max):
        self.weapons.add_weapon(i,id_weapon,loading_time,nbr_spell_max)

    #def calculate_pos(self,xscreen,yscreen):
    #    return (self.pos_x*self.cell_size+xscreen,self.pos_y*self.cell_size+yscreen)

    def move(self,delta):
        self.pos_x = delta[0]
        self.pos_y = delta[1]





class Player_not_you(Mob) :

    def __init__(self,cell_size,pos, pseudo = "Coming soon",is_you = False):

        super().__init__(pos[0],pos[1],cell_size,size=(size_display.PLAYER_SIZE_WIDTH,size_display.PLAYER_SIZE_HEIGHT))

        self.pseudo = pseudo
        self.is_you = is_you
        self.frame_perso_left = []
        self.frame_perso_right = []
        self.img_weapon = "incoming"
        self.angle = 90
        self.frame_weapon = []
        self.frame = 0
        self.frame_multiplier = 0

        self.cell_size=cell_size

        self.init_Img(cell_size)

    def init_Img(self,cell_size):
        for i in range(4):
            Img = pygame.image.load(assets.PLAYER_IDLE+f"{i+1}"+".png").convert_alpha() #convert_alpha() pour le fond vide
            Img = pygame.transform.scale(Img,(self.width*cell_size,self.height*cell_size))
            Img_flip = pygame.transform.flip(Img, True, False)
            self.frame_perso_right.append(Img)
            self.frame_perso_left.append(Img_flip)

    def update_frame(self):
        self.frame_multiplier +=1
        if self.frame_multiplier >= 100 :
            self.frame +=1
            self.frame_multiplier = 0

    def draw(self,screen,xscreen,yscreen):
        
        pos = self.calculate_pos_blit(xscreen,yscreen)
        #self.angle = self.get_angle(center, mouse_pos)
        
        perso_right = self.frame_perso_right[self.frame%4]
        perso_left = self.frame_perso_left[self.frame%4]
        self.dr_weapon = self.frame_weapon[self.frame%6]

        if 90<self.angle%360<270: #affiche le perso regardant une dirrection en fonction de la souris
            screen.blit(perso_right,pos)
        else :
            screen.blit(perso_left, pos)

        self.draw_weapon(screen,pos)

        self.update_frame()

        self.update_angle()

    def update_angle(self):
        self.angle+=1

    def draw_weapon(self,screen,pos):

        rotated_img = pygame.transform.rotate(self.dr_weapon, self.angle)
        rotated_polish = rotated_img.get_rect(center = pos)
        screen.blit(rotated_img, rotated_polish.topleft)

    def add_weapon(self,id_weapon):

        for i in range(4):
            img_weapon = pygame.image.load(assets.RANGED_WEAPON+f"{id_weapon}_{i}"+".png").convert_alpha()
            img_weapon = pygame.transform.scale(img_weapon,(weapon.HEIGHT_WEAPON1*self.cell_size,weapon.WIDTH_WEAPON1*self.cell_size))
            self.frame_weapon.append(img_weapon)

        for i in range(2, 0, -1):
            img_weapon = pygame.image.load(assets.RANGED_WEAPON+f"{id_weapon}_{i}"+".png").convert_alpha()
            img_weapon = pygame.transform.scale(img_weapon,(weapon.HEIGHT_WEAPON1*self.cell_size,weapon.WIDTH_WEAPON1*self.cell_size))
            self.frame_weapon.append(img_weapon)
        #self.img_weapon = pygame.image.load(assets.RANGED_WEAPON+f"{id_weapon}.png").convert_alpha()
        #self.img_weapon = pygame.transform.scale(self.img_weapon,(weapon.HEIGHT_WEAPON1*self.cell_size, weapon.WIDTH_WEAPON1*self.cell_size))

    def move(self,delta):
        self.pos_x = delta[0]
        self.pos_y = delta[1]
        


