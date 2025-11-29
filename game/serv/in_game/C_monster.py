from serv.in_game.C_mobs import mobs

class Skeleton(mobs):
    def __init__(self, x,y, id):
        self.name = "Skeleton"
        self.id = id
        self.pos_x = x
        self.pos_y = y
        
    def move(self,cells_arr,cell_dur,cell_vide,cell_liquid):
        """Logique de déplacement du monstre"""

        #cells_arr[y,x] te donne le type de cellule à la position (x,y) : Ex : 0=air, 1=sol, 2=eau, etc.
        #cell_dur / vide / liquid continent en 0 le min et en 1 le max du type de cell par ex dur : [2,5] signifie que les cellules de type 2 à 5 sont considérées comme dures
        #Peut donc faire : if self.is_type(cells_arr[self.pos_y,self.pos_x],cell_dur): pour savoir si cells_x,y est dur

        self.pos_x -= 1  # Exemple simple : le squelette se déplace vers la droite
        self.pos_y+=1


    def is_type(self, type_cell, type_check):
        """Vérifie si la cellule à la position (x,y) est du type spécifié"""
        if type_check[0] <= type_cell <= type_check[1]:
            return True
        return False