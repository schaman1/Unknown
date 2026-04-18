import pygame
from client.config import assets#,weapon

class Animation:

    def __init__(self,entity_name,cell_size,width,height):

        self.animation = {"running":{"right":[],
                                     "left":[],
                                     "time":0.1},
                          "idle":{"right":[],
                                  "left":[],
                                  "time":0.2},
                            "damage":{"duree":0.2,
                                      "time":0.2}}
        self.state = "idle"
        self.direction = "right"

        self.damage = False

        self.width = width*cell_size*2
        self.height = height*cell_size*2

        self.time_start_frame=0
        self.frame = 0

        self.init_animation(entity_name)

    def init_animation(self,entity_name):

        if entity_name == "player":

            #size_img = 50*cell_size
            size = self.width//2
            img_idle = pygame.image.load(assets.PLAYER_IDLE)
            img_idle = pygame.transform.scale(img_idle,(self.width,self.height))
            self.decoupe_img(img_idle,self.animation["idle"],size)

            img_running = pygame.image.load(assets.PLAYER_RUNNING)
            img_running = pygame.transform.scale(img_running,(self.width,self.height))
            self.decoupe_img(img_running,self.animation["running"],size)

        elif entity_name == "pnj" :

            #size_img = 50*cell_size
            size = self.width//2
            img_idle = pygame.image.load(assets.PNJ_IDLE)
            img_idle = pygame.transform.scale(img_idle,(self.width,self.height))
            self.decoupe_img(img_idle,self.animation["idle"],size)

            #img_running = pygame.image.load(assets.PLAYER_RUNNING)
            #img_running = pygame.transform.scale(img_running,(self.width,self.height))
            #self.decoupe_img(img_running,self.animation["running"],size)

    def decoupe_img(self,img,dest,size):
        for i in range(0,img.get_height(),size):
            for j in range(0,img.get_width(),size):

                rect = pygame.Rect(j,i,size,size)
                sub_img = img.subsurface(rect).copy()
                #sub_img = p
                sub_img_flip = pygame.transform.flip(sub_img,True,False)
                dest["left"].append(sub_img)
                dest["right"].append(sub_img_flip)

    def update_state(self,new_state):

        self.state = new_state

    def update_direction(self,new_direction):
        
        self.direction=new_direction

    def draw(self,dt,pos_blit,screen):
        self.time_start_frame+=dt

        if self.animation[self.state]["time"]<self.time_start_frame:

            self.time_start_frame-=self.animation[self.state]["time"]
            self.frame = (self.frame+1)%4

        img = self.animation[self.state][self.direction][self.frame]

        img = self.check_draw_red_if_damage(img,dt)

        screen.blit(img,pos_blit)

    def check_draw_red_if_damage(self,img,dt):

        if not self.damage :
            return img
        
        else:

            self.animation["damage"]["duree"]-=dt
        
            if self.animation["damage"]["duree"]<0:

                self.damage = False
                self.animation["damage"]["duree"] = self.animation["damage"]["time"]

            tmp = pygame.Surface.copy(img)
            tmp.fill((255,102,85),special_flags=pygame.BLEND_RGB_MULT)
            return tmp
        




    

        