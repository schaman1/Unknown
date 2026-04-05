import pygame, math
from client.domain.mob.mob import Mob
from client.config.display_text import FONT
from client.config import size_display
from client.domain.weapon.weapon_manager import WeaponManager

class Player_you(Mob) :

    def __init__(self,cell_size,pos,screen_size, pseudo = "Coming soon",is_you = True, money = 0):

        super().__init__(pos[0],pos[1],cell_size,size=(size_display.PLAYER_SIZE_WIDTH,size_display.PLAYER_SIZE_HEIGHT))

        self.money = money
        self.pseudo = pseudo
        self.is_you = is_you

        self.font = FONT
        self.text_money_color = (250,250,250)
        self.pos_money = (screen_size[0]//2,screen_size[1]*0.85)
        self.pos_blit_text = [None,None]
        self.text_money = self.font.render(str(self.money),True, self.text_money_color)  # True = anti-aliasing

        self.padding_life = 0.02
        self.key_active = {"right":False,
                           "left":False}

        #self.frame_weapon = []
        self.frame = 0
        self.frame_multiplier = 0

        self.rect_black_life = pygame.Rect(screen_size[0]//4,screen_size[1]*0.90, (screen_size[0]/2), screen_size[1]*0.03)

        self.weapons = WeaponManager()

        self.update_pos_blit_money()
    
    def get_angle(self, pos, mouse_pos) -> int:
        '''renvoie l'angle entre le perso et la souris en int'''
        oppose = mouse_pos[1] - pos[1]
        adjacent = mouse_pos[0] - pos[0]
        mouse_angle = int(math.degrees(math.atan2(-oppose,adjacent))) #comme atan() mais en 2D
        return mouse_angle%360
    
    def update_money(self, money):
        '''valeur de money envoyée par le serv et récupérée par le client'''

        old_money = self.money
        self.money = money
        delta_money = self.money-old_money

        self.text_money = self.font.render(str(self.money),True, self.text_money_color)
        self.update_pos_blit_money()

        return delta_money

    def draw(self,screen,dt):

        self.animation.draw(dt,self.pos_blit,screen)

    def draw_utils(self,screen,screen_size):

        self.draw_life(screen,screen_size)
        self.draw_money(screen)

    def draw_life(self,screen,screen_size):

        #self.padding_life

        pygame.draw.rect( #Pour voir où le perso est en temps reel
            screen,
            (50,60,50),  # couleur (blanc)
            self.rect_black_life,
        )
        #print(self.life)

        pygame.draw.rect( #Pour voir où le perso est en temps reel
            screen,
            (147,165,149),  # couleur (blanc)
            pygame.Rect(screen_size[0]//4,screen_size[1]*0.90, self.life*(screen_size[0]/2)//100, screen_size[1]*0.03)
        )

    def draw_money(self, screen):

        screen.blit(self.text_money, self.pos_blit_text)

    def update_pos_blit_money(self):
        size = FONT.size(str(self.money))
        self.pos_blit_text = [self.pos_money[0]+size[0]//2,self.pos_money[1]+size[1]//2]

    def draw_weapon(self,screen,angle,pos_draw) :

        self.weapons.draw_weapon(screen,angle,pos_draw, self.frame)

    def add_weapon(self,i,id_weapon,nbr_spell_max,spells_id,screen_size):
        self.weapons.add_weapon(i,id_weapon,nbr_spell_max,spells_id,screen_size)

    def add_spell(self,id_weapon,id_spell,pos_spell):

        self.weapons.lWeapons[id_weapon].add_spell(id_spell,pos_spell)

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


