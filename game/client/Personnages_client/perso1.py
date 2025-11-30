import pygame

class Player :
    '''
    Classe de test pour le perso de base
    '''

    def __init__(self,Img_perso,cell_size,pos_x = 500, pos_y=500):
        self.pos_x = pos_x
        self.pos_y = pos_y
        Img = pygame.image.load(Img_perso).convert() #convert_alpha() pour le fond vide
        self.Img_perso= pygame.transform.scale(Img,(10*cell_size,10*cell_size))
        pass

    def deplacement_basic(self):
        touche = pygame.key.get_pressed()
        #if touche[pygame.K_]
        pass

#player = Player(x,y,img)
#player.pos_x

#player2 = Player(x,y)
#player2.pos_x
