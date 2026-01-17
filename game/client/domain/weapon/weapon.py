import pygame,time
from client.config import assets,weapon
from shared.constants.world import CELL_SIZE

class Weapon :

    def __init__(self,id_weapon,loading_time,nbr_spell_max):

        self.loading_time = loading_time
        self.id_weapon = id_weapon
        self.nbr_spell_max = nbr_spell_max
        self.next_allowed_shot = 0

        self.img_weapon = pygame.image.load(assets.RANGED_WEAPON+f"{id_weapon}.png").convert_alpha() #pour l'instant c'est juste un projectile
        self.img_weapon = pygame.transform.scale(self.img_weapon,(weapon.HEIGHT_WEAPON1*CELL_SIZE, weapon.WIDTH_WEAPON1*CELL_SIZE)) #Setup sa taille après 

    def draw(self,screen,angle,pos_player):
        '''modifie l'orientation de l'arme en fonction de l'angle de la souris'''
        rotated_img = pygame.transform.rotate(self.img_weapon, angle)
        rotated_polish = rotated_img.get_rect(center = pos_player)
        screen.blit(rotated_img, rotated_polish.topleft)

    def update_next_allowed_shot(self):

        now = time.perf_counter()

        self.next_allowed_shot = now+self.loading_time/1000