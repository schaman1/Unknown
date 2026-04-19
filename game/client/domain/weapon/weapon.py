import pygame
from client.config import size_display as size
from client.config.display_text import FONT_SMALL
from client.domain.weapon.timer_spell import Timer
from client.ui.spell import Spell

class Weapon :

    def __init__(self,id_weapon,nbr_spell_max,spells_id,idx,screen_size,text):

        self.id_weapon = id_weapon
        self.idx = idx
        self.nbr_spell_max = nbr_spell_max
        self.frame_weapon = []
        self.spells_id = spells_id
        self.nbr_spell_stock=len(self.spells_id)
        self.icone_size=size.CELL_SIZE*4

        self.text_color = (250,250,250)
        self.text = text
        self.text_blit = FONT_SMALL.render(str(text),True, self.text_color)

        #self.imgs_spells = [None for _ in range(self.nbr_spell_stock)]
        self.spells=[None for _ in range(self.nbr_spell_stock)]
        #print(self.spells_id,"nbr max")
        self.load_spells(idx,screen_size)

        self.timer = Timer(idx,screen_size,text)

        self.screen_size = screen_size

    def load_spells(self,idx,screen_size):

        for j,id in enumerate(self.spells_id) :

            #img = pygame.image.load(assets.SPELLS[id]).convert_alpha()
            #img = pygame.transform.scale(img,(self.icone_size//2,self.icone_size))
            x=self.return_posx_blit_spell(screen_size,j)
            y=self.return_posy_blit_weapon(screen_size,idx)
            y_padding = y+0.25*self.icone_size
            self.spells[j]=Spell(id,x,y_padding,idx,j)

    def add_spell(self,id_spell,pos_spell):

        x=self.return_posx_blit_spell(self.screen_size,pos_spell)
        y=self.return_posy_blit_weapon(self.screen_size,self.idx)
        y_padding = y+0.25*self.icone_size
        self.spells[pos_spell]=Spell(id_spell,x,y_padding,self.idx,pos_spell)

    def draw_spells(self,screen,screen_size,i):

        y = self.return_posy_blit_weapon(screen_size,i)
        
        pygame.draw.rect( #bANDE noir
            screen,
            (14,16,14),  # couleur (blanc)
            pygame.Rect(screen_size[0]//4,y, screen_size[0]//2, 1.5*self.icone_size),
        )

        size_text = FONT_SMALL.size(str(self.text))
        #pos = pos_object[0]+self.size_img[0]//2 - size_text[0]//2,pos_object[1]+self.size_img[1]
        pos_text = (screen_size[0]//4 - size_text[0],y+0.5*self.icone_size)
        screen.blit(self.text_blit,pos_text)
        
        #print(self.spells_id)

        for j in range(self.nbr_spell_stock) :

            #x=self.return_posx_blit_spell(screen_size,j)

            #screen.blit(self.icone_spell,(x,y))

            if self.spells[j]!=None:

                self.spells[j].draw(screen)
            #if self.imgs_spells[j]!=None:
#
            #    screen.blit(self.imgs_spells[j],(x+self.icone_size//4,y+self.icone_size//4))

    def return_posy_blit_weapon(self,screen_size,i):

        return screen_size[1]/10+2*i*(self.icone_size)

    def return_posx_blit_spell(self,screen_size,i):
        padding = screen_size[0]/50

        return screen_size[0]//4 + padding + self.icone_size * i
    

    def draw_timer(self,screen,time):

        self.timer.draw(screen,time)
