import pygame
from client.config import assets

class Weapon :

    def __init__(self,id_weapon,loading_time,nbr_spell_max,cell_size):

        self.loading_time = loading_time
        self.id_weapon = id_weapon
        self.nbr_spell_max = nbr_spell_max

        self.img_weapon = pygame.image.load(assets.PIOCHE).convert_alpha() #pour l'instant c'est juste un projectile
        self.img_weapon = pygame.transform.scale(self.img_weapon,(5*cell_size, 5*cell_size)) #Setup sa taille après 

    def draw(self,screen,mouse_pos,center):
        '''modifie l'orientation de l'arme en fonction de l'angle de la souris'''
        self.angle = self.get_angle(center, mouse_pos)
        rotated_img = pygame.transform.rotate(self.img_weapon, self.angle)
        rotated_polish = rotated_img.get_rect(center = center)
        screen.blit(rotated_img, rotated_polish.topleft)
        self.update_frame()