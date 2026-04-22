import pygame,os
from client.config import assets,size_display
from utils.aseprite_reader import AsepriteReader


class Animation:

    def __init__(self,entity_name,cell_size,width,height):

        self.animation = {"running":{"right":[],
                                     "left":[],
                                     "time":0.1},
                          "idle":{"right":[],
                                  "left":[],
                                  "time":0.2},
                            "damage":{"duree":0.2,
                                      "time":0.2},
                            "death":{"right":[],
                                     "left":[],
                                     "time":3},
                            "respawn":{"right":[],
                                       "left":[],
                                       "time":0.5}}


        self.state = "idle"
        self.direction = "right"

        self.damage = False
        self.red = (255,102,85)
        self.green = (85,255,102)
        self.color_take_damage = self.red

        self.width = width*cell_size
        self.height = height*cell_size

        self.time_start_frame=0
        self.frame = 0

        self.fct_to_do = self.do_nothing

        self.init_animation(entity_name,cell_size)

    def add_tombe(self,cell_size):
            
        #Set die img

        height = int(self.height)
        delta = size_display.TOMBE_SIZE_WIDTH/size_display.TOMBE_SIZE_HEIGHT
        width = int(self.height*delta)

        Img = pygame.image.load(assets.MONSTER_DIE)
        Img = pygame.transform.scale(Img, (width,height))
        Img_flip = pygame.transform.flip(Img,True,False)
        self.animation["death"]["right"].append(Img)
        self.animation["death"]["left"].append(Img_flip)

        size = (width,height)
        img_idle = pygame.image.load(assets.TOMBE_DESTROY)
        img_idle = pygame.transform.scale(img_idle,(width*2,height*2)) #*2 car en a 2 par ligne
        self.decoupe_img(img_idle,self.animation["respawn"],size)

    def init_animation(self,entity_name,cell_size):

        if entity_name == "player":

            #size_img = 50*cell_size
            size = (self.width,self.height)
            img_idle = pygame.image.load(assets.PLAYER_IDLE)
            img_idle = pygame.transform.scale(img_idle,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["idle"],size)

            img_running = pygame.image.load(assets.PLAYER_RUNNING)
            img_running = pygame.transform.scale(img_running,(self.width*2,self.height*2))
            self.decoupe_img(img_running,self.animation["running"],size)

            self.add_tombe(cell_size)

        elif entity_name == "pnj" :

            #size_img = 50*cell_size
            size = (self.width,self.height)
            img_idle = pygame.image.load(assets.PNJ_IDLE)
            img_idle = pygame.transform.scale(img_idle,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["idle"],size)

            #img_running = pygame.image.load(assets.PLAYER_RUNNING)
            #img_running = pygame.transform.scale(img_running,(self.width,self.height))
            #self.decoupe_img(img_running,self.animation["running"],size)

        elif entity_name == "Skeleton":

            #self.decoupe_img(img_idle,self.animation["idle"],size)

            aseprite_path = assets.MONSTER_SKELETON
            #self.state = "death"
            
            if os.path.exists(aseprite_path):
                try:
                    reader = AsepriteReader(aseprite_path)
                    if reader.frames:
                        for surface in reader.frames:
                            Img = pygame.transform.scale(surface, (self.width,self.height))
                            Img_flip = pygame.transform.flip(Img,True,False)
                            self.animation["idle"]["right"].append(Img)
                            self.animation["idle"]["left"].append(Img_flip)
                            #self.frame_perso.append(scaled_surf)

                except Exception as e:
                    print(f"Failed to load aseprite: {e}")

            self.add_tombe(cell_size)

            print("Animation skeleton :",self.animation["death"])       

    def decoupe_img(self,img,dest,size):
        for i in range(0,img.get_height(),size[1]):
            for j in range(0,img.get_width(),size[0]):

                rect = pygame.Rect(j,i,size[0],size[1])
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

            self.frame = (self.frame+1)%len(self.animation[self.state]["right"])
            
            if self.frame == 0:
                self.fct_to_do()


        #print(self.frame,self.state,self.direction,"frame",self.animation[self.state][self.direction])
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
            tmp.fill(self.color_take_damage,special_flags=pygame.BLEND_RGB_MULT)
            return tmp
        
    def update_color(self,delta):

        self.damage = True

        if delta>=0 :
            self.color_take_damage = self.red
        else :
            self.color_take_damage = self.green

        self.animation["damage"]["duree"] = self.animation["damage"]["time"]

    def do_nothing(self):
        pass

    def end_respawn(self):
        self.state = "idle"
        self.fct_to_do = self.do_nothing

    def end_death(self):
        self.state = "respawn"
        self.fct_to_do = self.end_respawn

    def set_to_death(self,duree):
        self.animation["death"]["time"]=duree-2 #1 car les 4 frames de respawn durent 1 sec

        self.state = "death"
        self.frame = 0
        self.time_start_frame = 0
        self.fct_to_do = self.end_death