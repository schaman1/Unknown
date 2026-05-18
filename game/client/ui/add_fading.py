import pygame

class Fading:

    def __init__(self,screenSize):

        self.values = {"start":0,
                       "end":0,#Value to enter
                       "alpha":0,
                       "wait":0, #time to wait before fading
                       "on":False
                       }
        
        self.fading_layer = pygame.Surface(screenSize,pygame.SRCALPHA)
        
    def set_values(self,len_fading,wait_before_fade=0):

        self.values["end"]=len_fading*2 #*2 bcs white to black then black to white
        self.values["start"] = 0
        self.values["alpha"] = 0
        self.values["wait"] = wait_before_fade
        self.values["on"] = True

    def trigger(self,screen,dt):

        if self.values["on"] :

            if self.values["wait"]>0 :
                self.values["wait"]-=dt
                if self.values["wait"]<0:
                    self.values["wait"]=0

            else :

                self.values["start"]+=dt

                if self.values["start"]>self.values["end"]:
                    self.values["on"] = False
                    self.values["alpha"] = 0

                elif self.values["start"]<self.values["end"]/2 :

                    self.values["alpha"] = self.values["start"] * 255/(self.values["end"]/2)

                else :

                    self.values["alpha"] = (self.values["end"]-self.values["start"]) * 255/(self.values["end"]/2)

            self.fading_layer.fill((0,0,0,self.values["alpha"]))
            screen.blit(self.fading_layer,(0,0))