import pygame

class interactable:

    def __init__(self,pos_x,pos_y,price=0):
        #Pos finale

        self.img = None
        self.size_img = (None,None)

        self.pos_x = pos_x
        self.pos_y = pos_y

    def blit(self,screen,x,y):

        pos = self.ret_pos_blit(x,y)
        screen.blit(self.img,pos)

    def init_img(self,path):
        self.img = pygame.image.load(path)
        self.img = pygame.transform.scale(self.img,self.size_img)

    def ret_pos_blit(self,x,y):

        return self.pos_x+x-self.size_img[0]//2,self.pos_y+y-self.size_img[1]//2