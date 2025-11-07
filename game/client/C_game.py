import pygame
import var

class Game :
    """Class utilise quand lance le jeu / Permet d'afficher le jeu en gros et devra mettre plus tard les persos à afficher"""
    def __init__(self, size,canva_size):
        self.canva_size = canva_size
        self.cell_size = (self.canva_size[1]*var.cell_size)//var.serv_size[1]
        print(canva_size)
        self.canva = pygame.Surface(canva_size, pygame.SRCALPHA)
        #self.canva_map = self.map.canva
        self.bg = pygame.image.load("assets/bg1.png").convert()


        # pré-calcul des rects pour chaque cellule
        self.rect_grid = [
            [pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
             for x in range(self.canva_size[0]//self.cell_size +1)]
            for y in range(self.canva_size[1]//self.cell_size +1)
        ]
    
    def update_canva(self,l):
        """Reçoit les données l du serveur et appelle update"""
        for e in l :
            self.switch_cell(e)

    def switch_cell(self,el):
        """Chaque donné contient le x/y et les couleurs = dessine sur le canva !IMPORTANT : dessine pas sur le screen"""
        #print(el)
        x,y,r,g,b,a = el
        color = (r,g,b,a)
        #x,y,color = el
        #print(color)
        #try : 
        self.canva.fill(color, self.rect_grid[y][x])
        #except : 
        #    None
        #pygame.draw.rect(self.canva, color, self.rect_grid[y][x])