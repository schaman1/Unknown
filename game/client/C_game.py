import pygame
import var
#import mathFct as math

class Game :
    """Class utilise quand lance le jeu / Permet d'afficher le jeu en gros et devra mettre plus tard les persos à afficher"""
    def __init__(self, cell_size,canva_size):
        self.canva_size = canva_size
        self.cell_size = cell_size
        #print(self.cell_size,"Cell_size client")
        self.canva = pygame.Surface((canva_size[0]*cell_size,canva_size[1]*cell_size), pygame.SRCALPHA)
        #self.canva_map = self.map.canva
        self.bg = pygame.image.load("assets/bg1.png").convert()

        # pré-calcul des rects pour chaque cellule
        self.rect_grid = [
            [pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
             for x in range(var.serv_size[0])]
            for y in range(var.serv_size[1])
        ]


        #print(f"Nbr Y : {self.canva_size[1]//self.cell_size +1}, nbr X : {self.canva_size[0]//self.cell_size +1}")
    
    def update_canva(self,l):
        """Reçoit les données l du serveur et appelle update"""
        #print(l)
        for e in l :
            self.switch_cell(e)
        #self.canva.fill((255,0,0,255),self.rect_grid[2][2])

    def switch_cell(self,el):
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