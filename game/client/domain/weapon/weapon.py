import pygame
from client.config import assets,weapon,size_display as size
from client.ui.spell import Spell

class Weapon :

    def __init__(self,id_weapon,nbr_spell_max,spells_id,idx,screen_size):

        self.id_weapon = id_weapon
        self.nbr_spell_max = nbr_spell_max
        self.frame_weapon = []
        self.spells_id = spells_id
        self.nbr_spell_stock=len(self.spells_id)
        self.icone_size=size.CELL_SIZE*4

        for i in range(4):
            img_weapon = pygame.image.load(assets.RANGED_WEAPON[i]).convert_alpha()
            img_weapon = pygame.transform.scale(img_weapon,(weapon.HEIGHT_WEAPON1*size.CELL_SIZE,weapon.WIDTH_WEAPON1*size.CELL_SIZE))
            self.frame_weapon.append(img_weapon)

        for i in range(2, 0, -1):
            img_weapon = pygame.image.load(assets.RANGED_WEAPON[i]).convert_alpha()
            img_weapon = pygame.transform.scale(img_weapon,(weapon.HEIGHT_WEAPON1*size.CELL_SIZE,weapon.WIDTH_WEAPON1*size.CELL_SIZE))
            self.frame_weapon.append(img_weapon)

        self.icone_weapon = pygame.image.load(assets.RANGED_WEAPON[i]).convert_alpha()
        self.icone_weapon = pygame.transform.scale(self.icone_weapon,(self.icone_size,self.icone_size))

        #self.icone_spell = pygame.image.load(assets.ICONE_SPELL).convert_alpha()
        #self.icone_spell = pygame.transform.scale(self.icone_spell,(self.icone_size,self.icone_size))

        #self.imgs_spells = [None for _ in range(self.nbr_spell_stock)]
        self.spells=[None for _ in range(self.nbr_spell_stock)]
        #print(self.spells_id,"nbr max")
        self.load_spells(idx,screen_size)

    def load_spells(self,idx,screen_size):

        for j,id in enumerate(self.spells_id) :

            #img = pygame.image.load(assets.SPELLS[id]).convert_alpha()
            #img = pygame.transform.scale(img,(self.icone_size//2,self.icone_size))
            x=self.return_posx_blit_spell(screen_size,j)
            y=self.return_posy_blit_weapon(screen_size,idx)
            y_padding = y+0.25*self.icone_size
            self.spells[j]=Spell(id,x,y_padding,idx,j)

    def draw(self,screen,angle,pos_player, frame):
        '''modifie l'orientation de l'arme en fonction de l'angle de la souris'''
        fr_weapon = self.frame_weapon[frame%6]
        rotated_img = pygame.transform.rotate(fr_weapon, angle)
        rotated_polish = rotated_img.get_rect(center = pos_player)
        screen.blit(rotated_img, rotated_polish.topleft)

    def draw_icone(self,screen,screen_size,i):

        pos=(screen_size[0]//4+(4*i+1)*size.CELL_SIZE,screen_size[1]*0.80)

        #screen.blit(self.icone_spell,pos)

        #pygame.draw.rect( #Pour voir où le perso est en temps reel
        #    screen,
        #    (14,16,14),  # couleur (blanc)
        #    pygame.Rect(screen_size[0]//4+(4*i+1)*size.CELL_SIZE,screen_size[1]*0.80, self.icone_size, self.icone_size),
        #)

        screen.blit(self.icone_weapon,(screen_size[0]//4+(4*i+1)*size.CELL_SIZE,screen_size[1]*0.80))

    def draw_spells(self,screen,screen_size,i):

        y = self.return_posy_blit_weapon(screen_size,i)
        
        pygame.draw.rect( #bANDE noir
            screen,
            (14,16,14),  # couleur (blanc)
            pygame.Rect(screen_size[0]//4,y, screen_size[0]//2, 1.5*self.icone_size),
        )
        
        #print(self.spells_id)

        for j in range(self.nbr_spell_stock) :

            #x=self.return_posx_blit_spell(screen_size,j)

            #screen.blit(self.icone_spell,(x,y))

            self.spells[j].draw(screen)
            #if self.imgs_spells[j]!=None:
#
            #    screen.blit(self.imgs_spells[j],(x+self.icone_size//4,y+self.icone_size//4))

    def return_posy_blit_weapon(self,screen_size,i):

        return screen_size[1]/10+2*i*(self.icone_size)

    def return_posx_blit_spell(self,screen_size,i):
        padding = screen_size[0]/50

        return screen_size[0]//4 + padding + self.icone_size * i
