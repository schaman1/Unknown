import pygame
from client.config import assets#,weapon

class Animation:

    def __init__(self,entity_name,cell_size,width,height):

        self.animation = {"running":{"right":[],
                                     "left":[],
                                     "time":1},
                          "idle":{"right":[],
                                  "left":[],
                                  "time":1}}
        self.current_state = "idle"
        self.direction = "right"
        self.width = width
        self.height = height

        self.time_start_frame=0
        self.frame = 0

        self.init_animation(entity_name,cell_size)

    def init_animation(self,entity_name,cell_size):

        if entity_name == "player":
            for i in range(4):
                Img = pygame.image.load(assets.PLAYER_IDLE[i]).convert_alpha() #convert_alpha() pour le fond vide
                Img = pygame.transform.scale(Img,(self.width*cell_size,self.height*cell_size))

                Img_flip = pygame.transform.flip(Img, True, False)
                self.animation["idle"]["left"].append(Img)
                self.animation["idle"]["right"].append(Img_flip)

    def update_state(self,new_state):

        self.current_state = new_state

    def update_direction(self,new_direction):
        
        self.direction=new_direction

    def draw(self,dt,pos_blit,screen):
        self.time_start_frame+=dt

        if self.animation[self.current_state]["time"]<self.time_start_frame:

            self.time_start_frame-=self.animation[self.current_state]["time"]
            self.frame = (self.frame+1)%4

        screen.blit(self.animation[self.current_state][self.direction][self.frame],pos_blit)

        