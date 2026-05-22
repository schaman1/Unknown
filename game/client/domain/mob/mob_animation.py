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
                            "in_death":{"right":[],
                                        "left":[],
                                        "time":0
                                        },
                            "death":{"right":[],
                                     "left":[],
                                     "time":0},
                            "loading":{"right":[],
                                       "left":[],
                                       "time":1/4,},
                            "attacking":{"right":[],
                                       "left":[],
                                       "time":1/4,},
                            "respawn":{"right":[],
                                       "left":[],
                                       "time":0},
                            "run away":{"right":[],
                                       "left":[],
                                       "time":0.1},
                                       }

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

            img_death = pygame.image.load(assets.PLAYER_DEATH)
            img_death = pygame.transform.scale(img_death,(self.width*2,self.height*2))
            self.decoupe_img(img_death,self.animation["in_death"],size)

            l = len(self.animation["in_death"]["right"])

            for i in range(l):
                self.animation["death"]["right"].append(self.animation["in_death"]["right"][l-1])
                self.animation["death"]["left"].append(self.animation["in_death"]["left"][l-1])

                self.animation["respawn"]["right"].append(self.animation["in_death"]["right"][l-i-1])
                self.animation["respawn"]["left"].append(self.animation["in_death"]["left"][l-i-1])

        elif entity_name == "pnj" :

            #size_img = 50*cell_size
            size = (self.width,self.height)
            img_idle = pygame.image.load(assets.PNJ_IDLE)
            img_idle = pygame.transform.scale(img_idle,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["idle"],size)

            #img_running = pygame.image.load(assets.PLAYER_RUNNING)
            #img_running = pygame.transform.scale(img_running,(self.width,self.height))
            #self.decoupe_img(img_running,self.animation["running"],size)

        elif entity_name == "Laseroide" :

            #size_img = 50*cell_size
            size = (self.width,self.height)
            img_idle = pygame.image.load(assets.MONSTER_2)
            img_idle = pygame.transform.scale(img_idle,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["idle"],size)

            #size_img = 50*cell_size
            size = (self.width,self.height)
            img_idle = pygame.image.load(assets.MONSTER_2)
            img_idle = pygame.transform.scale(img_idle,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["running"],size)

            #size_img = 50*cell_size
            size = (self.width,self.height)
            img_idle = pygame.image.load(assets.MONSTER_2)
            img_idle = pygame.transform.scale(img_idle,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["run away"],size)

            #size_img = 50*cell_size
            size = (self.width,self.height)
            img_idle_loading = pygame.image.load(assets.MONSTER_2_LOADING)
            img_idle = pygame.transform.scale(img_idle_loading,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["loading"],size)

            #size_img = 50*cell_size
            size = (self.width,self.height)
            for i in range(4):
                self.animation["attacking"]["right"].append(self.animation["loading"]["right"][3])
                self.animation["attacking"]["left"].append(self.animation["loading"]["left"][3])
            #img_idle_loading = pygame.image.load(assets.MONSTER_2_LOADING)
            #img_idle = pygame.transform.scale(img_idle_loading,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            #self.decoupe_img(img_idle,self.animation["attacking"],size)

            self.add_tombe(cell_size)

        elif entity_name == "Defendeur" :

            size = (self.width,self.height)
            img_idle = pygame.image.load(assets.DEFENDEUR_IDLE)
            img_idle = pygame.transform.scale(img_idle,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["idle"],size)

            img_attack = pygame.image.load(assets.DEFENDEUR_ATTACK)
            img_idle = pygame.transform.scale(img_attack,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["attacking"],size)

            img_attack = pygame.image.load(assets.DEFENDEUR_ATTACK)
            img_idle = pygame.transform.scale(img_attack,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["loading"],size)

            img_running = pygame.image.load(assets.DEFENDEUR_RUNNING)
            img_idle = pygame.transform.scale(img_running,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["running"],size)

            img_running = pygame.image.load(assets.DEFENDEUR_RUNNING)
            img_idle = pygame.transform.scale(img_running,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["run away"],size)

            self.add_tombe(cell_size)

        elif entity_name == "Foulli" :

            #size_img = 50*cell_size
            size = (self.width,self.height)
            img_idle = pygame.image.load(assets.FOULLI)
            img_idle = pygame.transform.scale(img_idle,(self.width,self.height)) #*2 car en a 2 par ligne
            self.animation["idle"]["right"] = [img_idle]
            self.animation["idle"]["left"] = [img_idle]

            #size_img = 50*cell_size
            size = (self.width,self.height)
            img_idle_loading = pygame.image.load(assets.FOULLI_ATTACK)
            img_idle = pygame.transform.scale(img_idle_loading,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["attacking"],size)

            self.add_tombe(cell_size)

        elif entity_name == "Escargot" :

            #size_img = 50*cell_size
            size = (self.width,self.height)
            img_idle_loading = pygame.image.load(assets.ESCARGOT_RUNNING)
            img_idle = pygame.transform.scale(img_idle_loading,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["running"],size)
            img_idle = pygame.image.load(assets.ESCARGOT_IDLE)
            img_idle = pygame.transform.scale(img_idle,(self.width,self.height)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["idle"],size)

            #size_img = 50*cell_size
            size = (self.width,self.height)
            img_idle_loading = pygame.image.load(assets.ESCARGOT_RUNNING)
            img_idle = pygame.transform.scale(img_idle_loading,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["idle"],size)

            self.add_tombe(cell_size)
        
        elif entity_name == "Limace" :

            #size_img = 50*cell_size
            size = (self.width,self.height)
            img_idle = pygame.image.load(assets.LIMACE_IDLE) #LIMACE_IDLE
            img_idle = pygame.transform.scale(img_idle,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["idle"],size)

            img_attack = pygame.image.load(assets.LIMACE_ATTACK) #LIMACE_ATTACK
            img_idle = pygame.transform.scale(img_attack,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["attacking"],size)

            #size_img = 50*cell_size
            size = (self.width,self.height)
            img_idle_loading = pygame.image.load(assets.LIMACE_RUNNING)
            img_idle = pygame.transform.scale(img_idle_loading,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["running"],size)

            #size_img = 50*cell_size
            size = (self.width,self.height)
            img_idle_loading = pygame.image.load(assets.LIMACE_RUNNING)
            img_idle = pygame.transform.scale(img_idle_loading,(self.width*2,self.height*2)) #*2 car en a 2 par ligne
            self.decoupe_img(img_idle,self.animation["loading"],size)
            #print("anim loading limace :",self.animation["loading"])

            self.add_tombe(cell_size)

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

        if self.animation[self.state]["time"]<=self.time_start_frame:

            self.time_start_frame-=self.animation[self.state]["time"]

            try :
                self.frame = (self.frame+1)%len(self.animation[self.state]["right"])
            except :
                print(self.state)
            
            if self.frame == 0:
                self.fct_to_do()

        #print(self.frame,self.state,self.direction,"frame",self.animation[self.state][self.direction])
        try :
            img = self.animation[self.state][self.direction][self.frame]
        except :
            print(self.state)

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

    def next_idle(self):
        """Respawn anim"""
        self.state = "idle"
        self.fct_to_do = self.do_nothing

    def next_running(self):
        """Respawn anim"""
        self.state = "running"
        self.fct_to_do = self.do_nothing

    def end_death(self):
        """When is dead, do it"""
        self.state = "respawn"
        self.fct_to_do = self.next_idle

    def end_in_death(self):
        """When died, anim"""
        self.state = "death"
        self.fct_to_do = self.end_death

    def set_to_death(self,duree,state_beginning):

        if state_beginning == "in_death":

            self.animation["in_death"]["time"]=0.2 #1 car les 4 frames de respawn durent 1 sec
            self.animation["death"]["time"]=(duree-0.2*4)/4 #a 0.2*2 de trop pour le fade in fade out
            self.animation["respawn"]["time"]=0.3 #1 car les 4 frames de respawn durent 1 sec
            self.fct_to_do = self.end_in_death

        elif state_beginning == "death":
            self.animation["death"]["time"] = (duree-0.3*4)
            self.animation["respawn"]["time"] = 0.3
            self.fct_to_do = self.end_death

        self.state = state_beginning
        self.frame = 0
        self.time_start_frame = 0

    def dead_state(self):
        if self.state == "in_death" or self.state == "death" or self.state == "respawn" :
            return True
        
        return False
    
    def set_state(self,state_name):
        """Set a specific state of anim if ! not death"""
        if not self.dead_state():
            self.state = state_name
            self.frame = 0