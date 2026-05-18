import pygame
from client.config.display_text import FONT_SMALL

class interactable:

    def __init__(self,pos_x,pos_y,price=0):
        #Pos finale

        self.img = None
        self.img_use = None
        self.stay_after_use = False
        self.bg = None
        self.img_trigger = []

        self.can_trigger = True

        self.len_anim = 0
        self.current_dt = 0
        self.current_idx = 0

        self.price = price
        self.price_color = (250,250,250)
        self.size_img = (None,None)
        self.delta_size_bg = None

        self.trigger = False
        
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.font = FONT_SMALL
        self.text_price = self.font.render(str(self.price),True, self.price_color)

    def start_anim_trigger(self):
        if self.img_trigger != [] :
            self.trigger = True

    def stop_anim_trigger(self):
        self.trigger = False
        self.current_dt = 0
        self.current_idx = 0

    def blit(self,screen,x,y,dt):

        pos = self.ret_pos_blit(x,y)

        if self.bg :
            pos_bg = [pos[0] - self.delta_size_bg,pos[1]-self.delta_size_bg]
            screen.blit(self.bg,pos_bg)

        if self.trigger :
            screen.blit(self.img_trigger[self.current_idx],pos)
            self.current_dt+=dt
            if self.current_dt>=self.len_anim:
                self.current_dt-=self.len_anim
                self.current_idx+=1
                if self.current_idx==4 :#Car tj 4 frame pr le moment
                    self.stop_anim_trigger()

        else :
            screen.blit(self.img,pos)

        self.blit_price(screen,pos)

    def blit_price(self,screen,pos_object):

        if self.price != 0:
            size_text = FONT_SMALL.size(str(self.price))
            pos = pos_object[0]+self.size_img[0]//2 - size_text[0]//2,pos_object[1]+self.size_img[1]

            screen.blit(self.text_price,pos)

    def init_use_img(self,path):
        self.img_use = pygame.image.load(path)
        self.img_use = pygame.transform.scale(self.img_use,self.size_img)
        self.stay_after_use = True
            
    def init_img(self,path,path_bg=None,path_trigger=None,len_anim = 0):
        self.img = pygame.image.load(path)
        self.img = pygame.transform.scale(self.img,self.size_img)

        if path_trigger!=None :
            self.len_anim = len_anim
            img = pygame.image.load(path_trigger)
            img = pygame.transform.scale(img,(self.size_img[0]*2,self.size_img[1]*2))
            self.decoupe_img(img,self.img_trigger,self.size_img)

        if path_bg!=None :
            self.bg = pygame.image.load(path_bg)
            size_bg = (self.size_img[0] + 2*self.delta_size_bg,self.size_img[1]+ 2*self.delta_size_bg)
            self.bg = pygame.transform.scale(self.bg,size_bg)

    def ret_pos_blit(self,x,y):

        return self.pos_x+x-self.size_img[0]//2,self.pos_y+y-self.size_img[1]//2
    
    def decoupe_img(self,img,dest,size):
        for i in range(0,img.get_height(),size[1]):
            for j in range(0,img.get_width(),size[0]):

                rect = pygame.Rect(j,i,size[0],size[1])
                dest.append(img.subsurface(rect).copy())

    def use(self):
        self.price = 0
        self.can_trigger = False
        self.img = self.img_use