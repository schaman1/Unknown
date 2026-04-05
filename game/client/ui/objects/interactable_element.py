import pygame
from client.config.display_text import FONT_SMALL

class interactable:

    def __init__(self,pos_x,pos_y,price=0):
        #Pos finale

        self.img = None
        self.price = price
        self.price_color = (250,250,250)
        self.size_img = (None,None)

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.font = FONT_SMALL
        self.text_price = self.font.render(str(self.price),True, self.price_color)

    def blit(self,screen,x,y):

        pos = self.ret_pos_blit(x,y)
        screen.blit(self.img,pos)

        self.blit_price(screen,pos)

    def blit_price(self,screen,pos_object):

        if self.price != 0:
            size_text = FONT_SMALL.size(str(self.price))
            pos = pos_object[0]+self.size_img[0]//2 - size_text[0]//2,pos_object[1]+self.size_img[1]

            screen.blit(self.text_price,pos)


    def init_img(self,path):
        self.img = pygame.image.load(path)
        self.img = pygame.transform.scale(self.img,self.size_img)

    def ret_pos_blit(self,x,y):

        return self.pos_x+x-self.size_img[0]//2,self.pos_y+y-self.size_img[1]//2