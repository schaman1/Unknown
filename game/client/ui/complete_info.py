from client.config.assets import COMPLETE_INFO_BG,SPELLS
from client.config.display_text import FONT,FONT_SMALL
import pygame,json

class CompleteInfo:

    def __init__(self,screen_size,cell_size):

        #self.screen_size = screen_size

        self.cell_size = cell_size

        self.size = (40*cell_size,30*cell_size)
        self.background = pygame.image.load(COMPLETE_INFO_BG)
        self.background = pygame.transform.scale(self.background,self.size)

        self.surface_text = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface_text.fill((0,0,0,0))

        self.pos_blit = [None,None]
        self.spell_id = None
        self.delta_x = 5*self.cell_size
        self.pos_img = [self.size[0]//10,self.size[0]//8]

        #-------TEXT---------#
        self.font_big = FONT
        self.font_small = FONT_SMALL
        self.pos_name = [self.size[0]//4,self.size[1]//6]
        self.pos_x_other_info = self.size[0]//4
        self.pos_y_other_info = self.size[1]//3
        self.delta_y_other_info = self.size[1]//9

        with open('client/ui/json/info_spell.json','r') as info :
            self.infos = json.load(info)

        #self.dist_interactable_max = cell_size*

    def start_draw_spell(self,spell):

        self.spell_id = spell.id_spell_draw
        self.pos_blit = [spell.pos_x+self.delta_x,spell.pos_y]
        self.init_surface(spell.id_spell_draw,"SPELL")

        if f"SPELL{spell.id_spell_draw}" in self.infos :
            self.init_text(self.infos[f"SPELL{spell.id_spell_draw}"])
        else :
            self.init_text(self.infos["UNKNOWN"]) #Pour tj afficher qqch

    def init_text(self,dico_info):

        text_name = self.font_big.render(dico_info["name"],True,(0,0,0))
        self.surface_text.blit(text_name,self.pos_name)
        #self.draw_text_center(text_name,self.pos_name)

        pos_y = self.pos_y_other_info

        if dico_info["description"][0]!="Nothing" :

            self.font_small.set_italic(True) #display description in italic

            for i in range(len(dico_info["description"])):

                text_desc = self.font_small.render(f"{dico_info["description"][i]}",True,(0,0,0))
                self.surface_text.blit(text_desc,(self.pos_x_other_info,pos_y))

                if(i!=len(dico_info["description"])-1):
                    pos_y+=self.delta_y_other_info//2

            pos_y+=self.delta_y_other_info

            self.font_small.set_italic(False)

        if dico_info["type"]=="projectile":

            text_life = self.font_small.render(f"duree : {dico_info["life"]}",True,(0,0,0))
            self.surface_text.blit(text_life,(self.pos_x_other_info,pos_y))
            pos_y+=self.delta_y_other_info

            text_life = self.font_small.render(f"vitesse : {dico_info["speed"]}",True,(0,0,0))
            self.surface_text.blit(text_life,(self.pos_x_other_info,pos_y))
            pos_y+=self.delta_y_other_info

            if dico_info["rebond"]==0:
                eph = "non"
            else :
                eph = "oui"
            text_life = self.font_small.render(f"rebond : {eph}",True,(0,0,0))
            self.surface_text.blit(text_life,(self.pos_x_other_info,pos_y))
            pos_y+=self.delta_y_other_info

        text_life = self.font_small.render(f"rechargement : {dico_info["time_reload"]} sec",True,(0,0,0))
        self.surface_text.blit(text_life,(self.pos_x_other_info,pos_y))
        #pos_y+=self.delta_y_other_info

    def draw_text_center(self,text,pos):

        size = text.get_size()

        self.surface_text.blit(text,(pos[0]-size[0]//2,pos[1]-size[1]//2))        

    def init_surface(self,id_element,type_element):

        self.surface_text.blit(self.background,(0,0))

        if type_element=="SPELL":
            image = pygame.image.load(SPELLS[id_element])
            image = pygame.transform.scale(image,(self.size[0]/8,self.size[0]/8))

        else:
            print("Unknown type element in client/ui/complete_info")

        self.surface_text.blit(image,self.pos_img)
    
    def stop_draw(self):
        self.spell_id = None

    def blit_info(self,screen,spell_touch):

        if spell_touch==None :
            self.stop_draw()
            return

        if spell_touch.id_spell_draw != self.spell_id:
            self.start_draw_spell(spell_touch)

        screen.blit(self.surface_text,self.pos_blit)
