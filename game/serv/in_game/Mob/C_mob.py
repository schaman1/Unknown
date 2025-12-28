import var

class Mob:

    def __init__(self,pos,hp = 100,id=None):
        self.pos_x = pos[0]
        self.pos_y = pos[1]

        self.screen_global_size = var.BG_SIZE_SERVER

        self.acceleration = 10
        self.base_movement = var.RATIO #C'est le mouv de base = si ajoute 100, se deplace de 1 carre plus vite

        self.vitesse_x = 10 #Not use now will have to implement it with max_vitesse_x
        self.vitesse_y = 20#Not use now will have to implement it with max_vitesse_y

        self.hp = hp
        self.id = id

    def convert_from_base(self,nbr):
        """Retourne le nbr en 1 pour 1"""
        return nbr//self.base_movement
    
    def convert_to_base(self,nbr):
        """Retourne le nbr en 1 pour 100 = la base du serv car peut pas travailler avec des chiffres à virgule !"""
        return nbr*self.base_movement

    def gravity_effect(self,grid_cell,cell_dur):

        if self.vitesse_y < 5*self.base_movement:
            self.vitesse_y += self.acceleration

    def collision_down(self,grid_cell,cell_dur):

        #for j in range(-1*self.base_movement,2*self.base_movement,self.base_movement): #A implementer

        pos_before = self.pos_y

        s = self.return_signe(self.vitesse_y)
        remaining = self.vitesse_y*s

        while remaining > 0 :

            dist = self.base_movement

            if self.touch_wall((self.base_movement)*s,0,grid_cell,cell_dur) :
                dist = self.base_movement - self.pos_y%self.base_movement -1

                if dist < remaining :
                    self.vitesse_y = 0

            #if self.vitesse_y != 10 :
            #    print("dist, rem",dist,remaining)
            #    print("pos",self.pos_y,self.vitesse_y)

            if dist < remaining :
                self.pos_y+=dist*s
            
            else :
                self.pos_y+= remaining*s

            remaining -= self.base_movement

        return self.pos_y - pos_before

    def collision_right(self,grid_cell,cell_dur):

        pos_before = self.pos_x

        s = self.return_signe(self.vitesse_x)
        remaining = self.vitesse_x*s

        while remaining > 0 :

            dist = self.base_movement

            if self.touch_wall(0,(self.base_movement+1*self.base_movement)*s,grid_cell,cell_dur) :
                dist = self.base_movement - self.pos_x%self.base_movement -1

            #print("dist, rem",dist,remaining)
            #print("pos",self.pos_y,self.vitesse_y)

            if dist < remaining :
                self.vitesse_x = 0
                self.pos_x+=dist*s
            
            else :
                self.pos_x+= remaining*s

            remaining -= self.base_movement

        return self.pos_x-pos_before
        
    def touch_wall(self,i,j,grid_cell,cell_dur):
        return self.is_type(grid_cell[self.convert_from_base(self.pos_y+i),self.convert_from_base(self.pos_x+j)],cell_dur)
    
    def touch_ground(self,grid_cell,cell_dur):
        j = -1*self.base_movement
        while j<2*self.base_movement and not self.touch_wall(100,j,grid_cell,cell_dur) :
            j+=self.base_movement

        if j==2*self.base_movement :
            return False
    
        else :
            return True

    def is_type(self, type_cell, type_check):
        """Vérifie si la cellule à la position (x,y) est du type spécifié"""
        if type_check[0] <= type_cell <= type_check[1]:
            return True
        return False
    
    def return_signe(self,e):
        if e<0:
            return -1
        else :
            return 1