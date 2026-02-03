import pygame
from client.config import assets,weapon,size_display as size

class Weapon :

    def __init__(self,id_weapon,nbr_spell_max,spells_id):

        self.id_weapon = id_weapon
        self.nbr_spell_max = nbr_spell_max
        self.frame_weapon = []
        self.spells_id = spells_id

        for i in range(4):
            img_weapon = pygame.image.load(assets.RANGED_WEAPON[i]).convert_alpha()
            img_weapon = pygame.transform.scale(img_weapon,(weapon.HEIGHT_WEAPON1*size.CELL_SIZE,weapon.WIDTH_WEAPON1*size.CELL_SIZE))
            self.frame_weapon.append(img_weapon)

        for i in range(2, 0, -1):
            img_weapon = pygame.image.load(assets.RANGED_WEAPON[i]).convert_alpha()
            img_weapon = pygame.transform.scale(img_weapon,(weapon.HEIGHT_WEAPON1*size.CELL_SIZE,weapon.WIDTH_WEAPON1*size.CELL_SIZE))
            self.frame_weapon.append(img_weapon)

        self.icone = pygame.image.load(assets.RANGED_WEAPON[i]).convert_alpha()
        self.icone = pygame.transform.scale(self.icone,(size.CELL_SIZE*4,size.CELL_SIZE*4))

    def draw(self,screen,angle,pos_player, frame):
        '''modifie l'orientation de l'arme en fonction de l'angle de la souris'''
        fr_weapon = self.frame_weapon[frame%6]
        rotated_img = pygame.transform.rotate(fr_weapon, angle)
        rotated_polish = rotated_img.get_rect(center = pos_player)
        screen.blit(rotated_img, rotated_polish.topleft)

    def draw_icone(self,screen,screen_size,i):

        pygame.draw.rect( #Pour voir où le perso est en temps reel
            screen,
            (14,16,14),  # couleur (blanc)
            pygame.Rect(screen_size[0]//4+(4*i+1)*size.CELL_SIZE,screen_size[1]*0.80, size.CELL_SIZE*4, size.CELL_SIZE*4),
        )

        screen.blit(self.icone,(screen_size[0]//4+(4*i+1)*size.CELL_SIZE,screen_size[1]*0.80))