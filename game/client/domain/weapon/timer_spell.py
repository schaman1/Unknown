import pygame
from client.config.display_text import FONT_SMALL

class Timer :

    def __init__(self,idx,screen_size,text):

        self.x,self.y = screen_size[0]*3/4 , screen_size[1]/15 * idx
        self.w,self.h = screen_size[0]/8 , screen_size[1]/30

        self.text_color = (250,250,250)
        self.text = text
        self.text_blit = FONT_SMALL.render(str(text),True, self.text_color)
        size_text = FONT_SMALL.size(str(self.text))
        self.pos_text = (self.x - size_text[0] - screen_size[0]/50,self.y + self.h//2)

        self.start_reload = 0
        self.time_reload = 0

        self.rect_border = pygame.Rect(self.x,self.y,self.w,self.h)
        self.color_rect = (100,100,100)

        self.padding = self.h//4
        self.rect_inside = pygame.Rect(self.x + self.padding//2,self.y+self.padding//2,self.w-self.padding,self.h - self.padding)
        self.color_rect_inside = (30,30,30)

    def update_delta_time(self,start,delta):

        self.start_reload = start
        self.time_reload = delta

    def update_w_timer(self,time):

        delta = time - self.start_reload
        alpha = delta/self.time_reload

        new_w = alpha*(self.w-self.padding)


        self.rect_inside.width = new_w

    def draw(self,screen,time):

        if time>self.start_reload+self.time_reload :
            return
        
        else :

            self.update_w_timer(time)

            pygame.draw.rect(
                screen,
                self.color_rect,
                self.rect_border
            )

            pygame.draw.rect(
                screen,
                self.color_rect_inside,
                self.rect_inside
            )


            screen.blit(self.text_blit,self.pos_text)
        

