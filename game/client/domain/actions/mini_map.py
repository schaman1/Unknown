import pygame

class MiniMap :

    def __init__(self,vision_size,map_seen,map_unseen,screen_size,cell_size):

        self.size_1_pixel = 240//30
        #screen_size
        #map_seen_size
        self.map_seen = pygame.image.load(map_seen).convert()
        self.reel_size_map = self.map_seen.get_size()
        self.scale = screen_size[0]/self.reel_size_map[0]

        self.map_seen = pygame.transform.scale(self.map_seen, (screen_size[0],self.reel_size_map[1]*self.scale))

        self.map_unseen = pygame.Surface((screen_size[0],screen_size[1]), pygame.SRCALPHA)
        self.map_unseen.fill((0,0,0))

        self.cell_size = cell_size
        self.vision = 20#vision_size
        self.draw = False

    def draw_circle(self,screen,color,pos,r,width=0):

        pygame.draw.circle(screen, color, pos, r, width)

    def draw_map(self,screen,pos):

        pos = [pos[0]//(4*self.size_1_pixel),pos[1]//(4*self.size_1_pixel)]

        pos[0] *=self.scale
        pos[1] *=self.scale
        self.draw_circle(self.map_unseen,(0,0,0,0),pos,self.vision)

        if self.draw :
            screen.blit(self.map_seen,(0,0))
            screen.blit(self.map_unseen,(0,0))