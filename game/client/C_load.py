import pygame,math

class Load :
    """Permet quand appele a chaque iteration de dessiner un cercle qui tourne (appele quand on attend le serv pour join"""
    def __init__(self,screen,nbr = 8, distance = 50, speed = 1):
        """Nbr correspond au nombre de cercle dessine, distance = distance du centre et speed bah speed"""
        self.nbr = nbr
        self.angle = 0
        self.screen = screen
        self.mid = (self.screen.get_rect().center)
        self.distance = distance
        self.speed = speed
        self.rotate_angle = 2*math.pi/720

    def draw(self):
        """Dessine le cercle"""
        for i in range(self.nbr):
            pygame.draw.circle(self.screen,(150,150,150),self.calcul_pos(i),self.radius)

    def calcul_pos(self,idx):
        """Calcul la pos de 1 rond à dessiner"""
        angle = self.angle + 2*math.pi/(self.nbr)*idx

        self.angle +=self.rotate_angle * self.speed

        x = math.cos(angle) * self.distance
        y = math.sin(angle) * self.distance

        return (x+ self.mid[0],y + self.mid[1])