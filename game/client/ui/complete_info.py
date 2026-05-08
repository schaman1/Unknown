from client.config.assets import COMPLETE_INFO_BG,SPELLS
import pygame

class CompleteInfo:

    def __init__(self,screen_size,cell_size):

        #self.screen_size = screen_size

        self.cell_size = cell_size

        self.size = (30*cell_size,20*cell_size)
        self.background = pygame.image.load(COMPLETE_INFO_BG)
        self.background = pygame.transform.scale(self.background,self.size)

        self.surface_text = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface_text.fill((0,0,0,0))

        self.pos_blit = [None,None]
        self.spell_id = None
        self.delta_x = 5*cell_size

        #self.dist_interactable_max = cell_size*

    def start_draw_spell(self,spell):

        self.spell_id = spell.id_spell_draw
        self.pos_blit = [spell.pos_x+self.delta_x,spell.pos_y]
        self.init_surface(spell.id_spell_draw,"SPELL")

    def init_surface(self,id_element,type_element):

        self.surface_text.blit(self.background,(0,0))

        if type_element=="SPELL":
            image = pygame.image.load(SPELLS[id_element])
            image = pygame.transform.scale(image,(self.size[0]/4,self.size[0]/4))

        else:
            print("Unknown type element in client/ui/complete_info")

        self.surface_text.blit(image,(self.size[1]/4,self.size[1]/4))
    
    def stop_draw(self):
        self.spell_id = None

    def blit_info(self,screen,spell_touch):

        if spell_touch==None :
            self.stop_draw()
            return
            

        if spell_touch.id_spell_draw != self.spell_id:
            self.start_draw_spell(spell_touch)

        screen.blit(self.surface_text,self.pos_blit)
