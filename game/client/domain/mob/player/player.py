import pygame, math
from client.domain.mob.mob import Mob
from client.config import size_display
from client.domain.weapon.weapon_manager import WeaponManager

class Player_you(Mob) :

    def __init__(self,cell_size,pos, pseudo = "Coming soon",is_you = True, money = 0):

        super().__init__(pos[0],pos[1],cell_size,size=(size_display.PLAYER_SIZE_WIDTH,size_display.PLAYER_SIZE_HEIGHT))

        self.pseudo = pseudo
        self.is_you = is_you

        self.padding_life = 0.02
        self.money = money
        self.key_active = {"right":False,
                           "left":False}

        #self.frame_weapon = []
        self.frame = 0
        self.frame_multiplier = 0

        self.weapons = WeaponManager()
    
    def get_angle(self, pos, mouse_pos) -> int:
        '''renvoie l'angle entre le perso et la souris en int'''
        oppose = mouse_pos[1] - pos[1]
        adjacent = mouse_pos[0] - pos[0]
        mouse_angle = int(math.degrees(math.atan2(-oppose,adjacent))) #comme atan() mais en 2D
        return mouse_angle%360
    
    def update_money(self, money):
        '''valeur de money envoyée par le serv et récupérée par le client'''
        self.money = money

    def draw(self,screen,dt):

        self.animation.draw(dt,self.pos_blit,screen)

    def draw_utils(self,screen,screen_size):

        self.draw_life(screen,screen_size)
        self.draw_money(screen,screen_size)

    def draw_life(self,screen,screen_size):

        #self.padding_life

        pygame.draw.rect( #Pour voir où le perso est en temps reel
            screen,
            (14,16,14),  # couleur (blanc)
            pygame.Rect(screen_size[0]//4,screen_size[1]*0.90, (screen_size[0]/2), screen_size[1]*0.03),
        )
        #print(self.life)

        pygame.draw.rect( #Pour voir où le perso est en temps reel
            screen,
            (147,165,149),  # couleur (blanc)
            pygame.Rect(screen_size[0]//4,screen_size[1]*0.90, self.life*(screen_size[0]/2)//100, screen_size[1]*0.03)
        )

    def draw_money(self, screen, screen_size):
        pygame.draw.rect(
            screen,
            (0,255,0),
            pygame.Rect(screen_size[0]//5, screen_size[1]//5, screen_size[0]//10, self.money*(screen_size[1]//10))
        )

    def draw_weapon(self,screen,angle,pos_draw) :

        self.weapons.draw_weapon(screen,angle,pos_draw, self.frame)

    def add_weapon(self,i,id_weapon,nbr_spell_max,spells_id,screen_size):
        self.weapons.add_weapon(i,id_weapon,nbr_spell_max,spells_id,screen_size)

    def shot(self,id_key):

        #return self.weapons.shot(self.angle_weapon)
        info = self.weapons.shot(id_key)
        if info != None :
            return self.weapons.shot(id_key)
        else :
            return

    def move(self,delta):
        self.pos_x = self.convert_from_base(delta[0]*self.cell_size)
        self.pos_y = self.convert_from_base(delta[1]*self.cell_size)

    def calcule_new_direction(self):
        if self.key_active["left"] and not self.key_active["right"] :
            self.animation.direction="left"
            self.animation.update_state("running")

        elif self.key_active["right"] and not self.key_active["left"]:
            self.animation.direction="right"
            self.animation.update_state("running")

        elif not self.key_active["right"] and not self.key_active["left"]:
            self.animation.update_state("idle")

    def update_direction_look(self,new_direction):
        
        if new_direction==None:
            return
        
        else :
            self.is_looking=new_direction
            if new_direction==0:
                self.key_active["right"]=True

            elif new_direction==2:
                self.key_active["left"]=True


            self.calcule_new_direction()

    def update_direction_stop_look(self,stop_direction):

            if stop_direction==0:
                self.key_active["right"]=False

            elif stop_direction==2:
                self.key_active["left"]=False

            self.calcule_new_direction()

class Player_not_you(Mob) :

    def __init__(self,cell_size,pos, pseudo = "Coming soon",is_you = False):

        super().__init__(pos[0],pos[1],cell_size,size=(size_display.PLAYER_SIZE_WIDTH,size_display.PLAYER_SIZE_HEIGHT))

        self.pseudo = pseudo
        self.is_you = is_you

        self.cell_size=cell_size

    def draw(self,screen,dt):
        
        #self.update_angle()

        #self.pos_blit = self.calculate_pos_blit(xscreen,yscreen)
        #self.angle = self.get_angle(center, mouse_pos)
#
        self.animation.draw(dt,self.pos_blit,screen)


    #def update_angle(self):
    #    self.angle+=1

    #def draw_weapon(self,screen,pos):
#
    #    rotated_img = pygame.transform.rotate(self.dr_weapon, self.angle)
    #    rotated_polish = rotated_img.get_rect(center = pos)
    #    screen.blit(rotated_img, rotated_polish.topleft)
#
    #def add_weapon(self,id_weapon):
#
    #    for i in range(4):
    #        img_weapon = pygame.image.load(assets.RANGED_WEAPON[i]).convert_alpha()
    #        img_weapon = pygame.transform.scale(img_weapon,(weapon.HEIGHT_WEAPON1*self.cell_size,weapon.WIDTH_WEAPON1*self.cell_size))
    #        self.frame_weapon.append(img_weapon)
#
    #    for i in range(2, 0, -1):
    #        img_weapon = pygame.image.load(assets.RANGED_WEAPON[i]).convert_alpha()
    #        img_weapon = pygame.transform.scale(img_weapon,(weapon.HEIGHT_WEAPON1*self.cell_size,weapon.WIDTH_WEAPON1*self.cell_size))
    #        self.frame_weapon.append(img_weapon)
#
    def move(self,delta):
        old_pos = self.pos_x
        
        self.pos_x = self.convert_from_base(delta[0]*self.cell_size)
        self.pos_y = self.convert_from_base(delta[1]*self.cell_size)

        delta_x = self.pos_x-old_pos

        if delta_x>=0:
            self.animation.direction = "right"

        else :
            self.animation.direction = "left"


