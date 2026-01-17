import pygame, math
from client.domain.mob.mob import Mob
from client.config import assets
from shared.constants import size_display

class Player(Mob) :

    def __init__(self,cell_size,pos, pseudo = "Coming soon",is_you = False):

        super().__init__(pos[0],pos[1],cell_size,size=(size_display.PLAYER_SIZE_WIDTH,size_display.PLAYER_SIZE_HEIGHT))

        self.pseudo = pseudo
        self.is_you = is_you
        self.frame_perso_left = []
        self.frame_perso_right = []
        #self.frame_weapon = []
        self.frame = 0
        self.frame_multiplier = 0

        self.init_Img(cell_size)

    def init_Img(self,cell_size):
        for i in range(4):
            img_left = pygame.image.load(assets.PLAYER_IDLE+f"{i+1}"+".png").convert_alpha() #convert_alpha() pour le fond vide
            img_left = pygame.transform.scale(img_left,(self.width*cell_size,self.height*cell_size))
            self.frame_perso_left.append(img_left)
            img_right = pygame.transform.flip(img_left, True, False)
            self.frame_perso_right.append(img_right) #liste d'image dans l'autre sens pour pas couper l'animation

        self.img_weapon = pygame.image.load(assets.RANGED_WEAPON+"2.png").convert_alpha()
        self.img_weapon = pygame.transform.scale(self.img_weapon,(self.width*16, self.height*16))


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
    
    def draw_weapon(self,screen,angle,pos):
        '''modifie l'orientation de l'arme en fonction de l'angle de la souris'''
        rotated_img = pygame.transform.rotate(self.img_weapon, angle)
        rotated_polish = rotated_img.get_rect(center = pos)
        screen.blit(rotated_img, rotated_polish.topleft)

    def draw(self,screen,xscreen,yscreen, mouse_pos=None,center=None):
        
        pos = self.calculate_pos_blit(xscreen,yscreen)
        self.angle_weapon = self.get_angle(pos, mouse_pos)
        #self.angle = self.get_angle(center, mouse_pos)
        
        perso_left = self.frame_perso_left[self.frame%4]
        perso_right = self.frame_perso_right[self.frame%4] 

        if mouse_pos[0] > center[0]: #affiche le perso regardant une dirrection en fonction de la souris
            screen.blit(perso_right,pos)
        else :
            screen.blit(perso_left, pos)
        self.update_frame()

        self.draw_weapon(screen,self.angle_weapon,pos)
        
        pygame.draw.rect( #Pour voir où le perso est en temps reel
            screen,
            (255, 255, 255),  # couleur (blanc)
            pygame.Rect((self.pos_x*self.cell_size)//100+xscreen, self.pos_y*self.cell_size//100+yscreen, self.cell_size, self.cell_size)
        )

    #def calculate_pos(self,xscreen,yscreen):
    #    return (self.pos_x*self.cell_size+xscreen,self.pos_y*self.cell_size+yscreen)

    def move(self,delta):
        self.pos_x = delta[0]
        self.pos_y = delta[1]
        

