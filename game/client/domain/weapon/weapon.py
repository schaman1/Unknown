import pygame
from client.config import assets,weapon
from shared.constants.world import CELL_SIZE

class Weapon :

    def __init__(self,id_weapon,nbr_spell_max,spells_id):

        self.id_weapon = id_weapon
        self.nbr_spell_max = nbr_spell_max
        self.frame_weapon = []
        self.spells_id = spells_id

        for i in range(4):
            img_weapon = pygame.image.load(assets.RANGED_WEAPON[i]).convert_alpha()
            img_weapon = pygame.transform.scale(img_weapon,(weapon.HEIGHT_WEAPON1*CELL_SIZE,weapon.WIDTH_WEAPON1*CELL_SIZE))
            self.frame_weapon.append(img_weapon)

        for i in range(2, 0, -1):
            img_weapon = pygame.image.load(assets.RANGED_WEAPON[i]).convert_alpha()
            img_weapon = pygame.transform.scale(img_weapon,(weapon.HEIGHT_WEAPON1*CELL_SIZE,weapon.WIDTH_WEAPON1*CELL_SIZE))
            self.frame_weapon.append(img_weapon)

    def draw(self,screen,angle,pos_player, frame):
        '''modifie l'orientation de l'arme en fonction de l'angle de la souris'''
        fr_weapon = self.frame_weapon[frame%6]
        rotated_img = pygame.transform.rotate(fr_weapon, angle)
        rotated_polish = rotated_img.get_rect(center = pos_player)
        screen.blit(rotated_img, rotated_polish.topleft)