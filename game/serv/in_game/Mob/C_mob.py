import var


class Mob:

    def __init__(self,pos,hp = 100,id=None):
        self.pos_x = pos[0]
        self.pos_y = pos[1]

        self.screen_global_size = var.BG_SIZE_SERVER

        self.acceleration = 1
        self.vitesse_x = 0
        self.vitesse_y = 0
        
        self.hp = hp
        self.id = id

    def gravity_effect(self,grid_cell,cell_dur):
        
        if self.vitesse_y < 5:
            self.vitesse_y += self.acceleration

        i=0
        while i<self.vitesse_y and not self.is_type(grid_cell[self.pos_y+i,self.pos_x],cell_dur) :
            i+=1
        
        if i != self.vitesse_y :
            self.vitesse_y=0


    def is_type(self, type_cell, type_check):
        """Vérifie si la cellule à la position (x,y) est du type spécifié"""
        if type_check[0] <= type_cell <= type_check[1]:
            return True
        return False