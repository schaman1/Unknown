from client.config import assets,size_display as size
import pygame

class Spell:

    def __init__(self,id,x,y,idx_weapon,idx_spell):

        self.pos_x = x
        self.pos_y = y
        self.idx_weapon=idx_weapon
        self.idx_spell=idx_spell

        #self.spell_id = id

        self.blit_icone = True

        self.icone_size=size.CELL_SIZE*4

        self.icone_spell = pygame.image.load(assets.ICONE_SPELL).convert_alpha()
        self.icone_spell = pygame.transform.scale(self.icone_spell,(self.icone_size,self.icone_size))

        self.img = None
        self.rect = self.icone_spell.get_rect(topleft = (self.pos_x,self.pos_y))
        self.load_image(id)

    def load_image(self,id_spell):

        if id_spell != 0:

            self.img = pygame.image.load(assets.SPELLS[id_spell]).convert_alpha()
            self.img = pygame.transform.scale(self.img,(self.icone_size//2,self.icone_size//2))

    def draw(self,screen):

        screen.blit(self.icone_spell,(self.pos_x,self.pos_y))


        if self.img!=None and self.blit_icone:

            screen.blit(self.img,(self.pos_x+self.icone_size//4,self.pos_y+self.icone_size//4))


