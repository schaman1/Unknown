import pygame, math
from client.domain.mob.mob import Mob
from client.config.display_text import FONT,FONT_SMALL
from client.config import size_display
from client.domain.weapon.weapon_manager import WeaponManager

class Player_you(Mob) :

    def __init__(self,cell_size,pos,screen_size, pseudo = "Coming soon",is_you = True, money = 0):

        super().__init__(pos[0],pos[1],cell_size,size=(size_display.PLAYER_SIZE_WIDTH,size_display.PLAYER_SIZE_HEIGHT))

        self.money = money
        self.pseudo = pseudo
        self.is_you = is_you

        self.font = FONT
        self.text_pseudo_color = (250,250,250)
        self.text_pseudo = FONT_SMALL.render(str(self.pseudo[:-7]),True, self.text_pseudo_color)  # True = anti-aliasing
        size = FONT_SMALL.size(str(self.pseudo[:-7]))
        self.delta_pos_pseudo = [-size[0]//2 + self.width//2*self.cell_size,0]

        self.text_life_color = (250,250,250)
        self.text_life = self.font.render(f"{self.life}/{self.max_life}",True, self.text_life_color)  # True = anti-aliasing
        
        self.text_money_color = (250,250,250)
        self.pos_money = (screen_size[0]//2,screen_size[1]*0.85)
        self.text_money = self.font.render(str(self.money),True, self.text_money_color)  # True = anti-aliasing
        self.pos_blit_text = [None,None]

        self.padding_life = 0.02
        self.key_active = {"right":False,
                           "left":False}

        #self.frame_weapon = []
        self.frame = 0
        self.frame_multiplier = 0

        self.rect_black_life = pygame.Rect(screen_size[0]//4,screen_size[1]*0.90, (screen_size[0]/2), screen_size[1]*0.03)

        self.weapons = WeaponManager(screen_size,cell_size)

        self.money_image = pygame.image.load("assets/sprites/ressources/money.png")
        self.money_image = self.money_image.convert_alpha()
        # self.money_image = pygame.transform.rotate(self.money_image, -30)
        self.money_image = pygame.transform.scale(self.money_image, (self.money_image.get_width() * 3, self.money_image.get_height() *3) )
        # self.money_image = self.money_image.

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

    def draw(self,screen,dt,xscreen,yscreen):

        self.update_interpolate_pos()

        self.update_pos_blit(xscreen,yscreen)

        self.animation.draw(dt,self.pos_blit,screen)

        self.draw_pseudo(screen,self.pos_blit)

    def draw_pseudo(self,screen,pos_blit):

        pos = [self.delta_pos_pseudo[0],self.delta_pos_pseudo[1]]
        pos[0]+=pos_blit[0]
        pos[1]+=pos_blit[1]
        screen.blit(self.text_pseudo, pos)

    def draw_utils(self,screen,screen_size):

        self.draw_life(screen,screen_size)
        self.draw_money(screen)

        self.weapons.draw_timer_all(screen)

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
            pygame.Rect(screen_size[0]//4,screen_size[1]*0.90, int(self.life/self.max_life*100)*(screen_size[0]/2)//100, screen_size[1]*0.03)
        )

        screen.blit(self.text_life, (screen_size[0]//4,screen_size[1]*0.90))

    def draw_money(self, screen):
        self.pos_blit_im_money = [self.pos_blit_text[0] - 90, self.pos_blit_text[1] - 30]

        screen.blit(self.money_image, self.pos_blit_im_money)
        screen.blit(self.text_money, self.pos_blit_text)

    def update_pos_blit_money(self):
        size = FONT.size(str(self.money))
        self.pos_blit_text = [self.pos_money[0],self.pos_money[1]]
        self.pos_blit_money = [self.pos_money[0]+size[0]//2,self.pos_money[1]]

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

    #def move(self,delta):
    #    self.pos_x = self.convert_from_base(delta[0]*self.cell_size)
    #    self.pos_y = self.convert_from_base(delta[1]*self.cell_size)

    def calcule_new_direction(self):
        """Update l'anim si pas dans un dead state"""

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

    def move(self,delta):
        new_pos = self.convert_from_base(delta[0]*self.cell_size),self.convert_from_base(delta[1]*self.cell_size)
        self.move_mob(new_pos)

    def kill(self,duree):

        self.animation.set_to_death(duree,"in_death")

class Player_not_you(Mob) :

    def __init__(self,cell_size,pos, pseudo = "Coming soon",is_you = False):

        super().__init__(pos[0],pos[1],cell_size,size=(size_display.PLAYER_SIZE_WIDTH,size_display.PLAYER_SIZE_HEIGHT))

        self.pseudo = pseudo
        self.is_you = is_you

        self.len_anim = {"running":0.2,
                         "idle":0, #Always idle when no state
                         }
        self.remaining_time_anim = 0

        self.old_state = "idle"

        self.text_pseudo_color = (250,250,250)
        self.text_pseudo = FONT_SMALL.render(str(self.pseudo),True, self.text_pseudo_color)  # True = anti-aliasing
        size = FONT_SMALL.size(str(self.pseudo))
        self.delta_pos_pseudo = [-size[0]//2 + self.width//2*self.cell_size,0]

        self.cell_size=cell_size

    def draw(self,screen,dt,xscreen,yscreen):
        
        #self.update_angle()

        #self.pos_blit = self.calculate_pos_blit(xscreen,yscreen)
        #self.angle = self.get_angle(center, mouse_pos)

        self.update_interpolate_pos()

        self.update_state_animation(dt)

        self.update_pos_blit(xscreen,yscreen)
#
        self.animation.draw(dt,self.pos_blit,screen)

        self.draw_pseudo(screen,self.pos_blit)

    def draw_pseudo(self,screen,pos_blit):

        pos = [self.delta_pos_pseudo[0],self.delta_pos_pseudo[1]]
        pos[0]+=pos_blit[0]
        pos[1]+=pos_blit[1]
        screen.blit(self.text_pseudo, pos)

    def move(self,delta):

        new_pos = self.convert_from_base(delta[0]*self.cell_size),self.convert_from_base(delta[1]*self.cell_size)
        
        if new_pos[0]-self.pos_x>0:
            self.animation.direction = "right"
            if self.old_state != "running" :
                self.old_state = "running"
                self.animation.set_state("running")
                self.remaining_time_anim = self.len_anim["running"]

        elif new_pos[0]-self.pos_x<0 :
            self.animation.direction = "left"
            if self.old_state != "running" :
                self.old_state = "running"
                self.animation.set_state("running")
                self.remaining_time_anim = self.len_anim["running"]

        self.move_mob(new_pos)

    def kill(self,duree):

        self.animation.set_to_death(duree,"in_death")

    def update_state_animation(self,dt):

        self.remaining_time_anim -= dt
        if self.remaining_time_anim<0:
            self.remaining_time_anim = 0

            if self.old_state != "idle" :
                self.old_state = "idle"
                self.animation.set_state("idle")