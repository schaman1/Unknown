import pygame

class MiniMap :

    def __init__(self,vision_size,map_seen,map_unseen,canva_size,cell_size):

        self.map_seen = pygame.image.load(map_seen).convert()
        self.map_seen = pygame.transform.scale(self.map_seen, (canva_size[0],canva_size[1]))

        self.map_unseen = pygame.Surface((canva_size[0],canva_size[1]), pygame.SRCALPHA)
        self.map_unseen.fill((0,0,0))


        self.cell_size = cell_size
        self.vision = vision_size
        self.draw = False

    def draw_circle(self,screen,color,pos,r,width=0):

        pygame.draw.circle(screen, color, pos, r, width)

    def draw_map(self,screen,pos):

        self.draw_circle(self.map_unseen,(0,0,0,0),pos,self.vision)

        if self.draw :
            screen.blit(self.map_seen,(0,0))
            screen.blit(self.map_unseen,(0,0))
