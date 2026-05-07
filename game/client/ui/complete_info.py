from client.config.assets import COMPLETE_INFO_BG,SPELLS
import pygame

class CompleteInfo:

    def __init__(self,screen_size,cell_size):

        self.draw = False
        #self.screen_size = screen_size

        self.cell_size = cell_size

        self.size = (30*cell_size,20*cell_size)
        self.background = pygame.image.load(COMPLETE_INFO_BG)
        self.background = pygame.transform.scale(self.background,self.size)

        self.surface_text = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface_text.fill((0,0,0,0))

        self.pos_blit = [0,0]
        self.dist_interactable_max = cell_size*2

        self.start_draw(3,"SPELL",[100,100])

    def start_draw(self,id_element,type_element,pos):
        self.draw = True

        self.pos_blit = pos
        self.init_surface(id_element,type_element)

    def init_surface(self,id_element,type_element):

        self.surface_text.blit(self.background,(0,0))

        if type_element=="SPELL":
            image = pygame.image.load(SPELLS[id_element])
            image = pygame.transform.scale(image,(self.size[0]/4,self.size[0]/4))

        else:
            print("Unknown type element in client/ui/complete_info")

        self.surface_text.blit(image,(self.size[1]/4,self.size[1]/4))

    def blit_info(self,screen):

        screen.blit(self.surface_text,self.pos_blit)
