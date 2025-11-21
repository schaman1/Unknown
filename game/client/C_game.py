import pygame
import var

class Game :
    """Class utilise quand lance le jeu / Permet d'afficher le jeu en gros et devra mettre plus tard les persos à afficher"""
    def __init__(self, cell_size,canva_size):
        self.canva_size = canva_size
        self.cell_size = cell_size
        self.center = (self.canva_size[0]//2,self.canva_size[1]//2)
        self.canva = pygame.Surface((canva_size[0]*cell_size,canva_size[1]*cell_size), pygame.SRCALPHA)
        #self.canva_map = self.map.canva
        self.bg = pygame.image.load("assets/bg1.png").convert()
        self.bg = pygame.transform.scale(self.bg, (canva_size[0],canva_size[1]))
        self.light = pygame.Surface((canva_size[0],canva_size[1]), pygame.SRCALPHA)
        self.create_light(vision = var.NBR_CELL_CAN_SEE)

        # pré-calcul des rects pour chaque cellule
        self.rect_grid = [
            [pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
             for x in range(var.BG_SIZE_SERVER[0])]
            for y in range(var.BG_SIZE_SERVER[1])
        ]


        #print(f"Nbr Y : {self.canva_size[1]//self.cell_size +1}, nbr X : {self.canva_size[0]//self.cell_size +1}")
    
    def update_canva(self,l):
        """Reçoit les données l du serveur et appelle update"""
        #print(l)
        for e in l :
            self.switch_cell(e)
        #self.canva.fill((255,0,0,255),self.rect_grid[2][2])

    def create_light(self,vision:int = 10 ):
        """Permet de faire genre que le personnage voit à une certaine portée"""
        self.light.fill((0,0,0))

        for i in range(10):
            pygame.draw.circle(self.light, (0,0,0,200 - (i+1)*20), self.center, (vision+2-i/5)*self.cell_size, width=0)

    def switch_cell(self,el:tuple):
        """Chaque donné contient le x/y et les couleurs = dessine sur le canva !IMPORTANT : dessine pas sur le screen"""

        x,y,r,g,b,a = el
        color = (r,g,b,a)
        #print(x,y) #!!!Le print alors que marche pas wtf
        #x,y,color = el

        #try : 

        self.canva.fill((0,255,0,255), pygame.Rect(500,500,50,50))
        self.canva.fill(color, self.rect_grid[y][x])
        #except : 
        #    None
        #pygame.draw.rect(self.canva, color, self.rect_grid[y][x])

    def draw(self,screen,x,y):
        screen.blit(self.bg,(0,0))
        screen.blit(self.canva, (x, y))
        screen.blit(self.light,(0,0))
        