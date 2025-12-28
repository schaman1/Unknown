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

        for j in range(-1*self.base_movement,2*self.base_movement,self.base_movement):

            s = self.return_signe(self.vitesse_y)
            i=(self.vitesse_y*s)%self.base_movement
            while i<=self.vitesse_y*s and not self.touch_wall(i*s,j+self.vitesse_x,grid_cell,cell_dur):#self.is_type(grid_cell[self.pos_y+i,self.pos_x],cell_dur) :
                i+=self.base_movement
            
            if i<=self.vitesse_y*s :

                if i >= self.base_movement: #Si bouge plus que d'un carreau
                    i-=self.base_movement

                self.vitesse_y = (i-i%self.base_movement+(-self.pos_y)%self.base_movement-1)*s

    def collision_right(self,grid_cell,cell_dur):

        s = self.return_signe(self.vitesse_x)
        i=(self.vitesse_x*s)%self.base_movement
        while i<=self.vitesse_x*s and not self.touch_wall(-self.base_movement,(i+1*self.base_movement)*s,grid_cell,cell_dur):
            i+=self.base_movement
        

        if i<=self.vitesse_x*s: #Pour faire en gros si touche un mur avec la vitesse x sans la y alors stoppe.
            #Au contraire, la y teste pas si touche le mur sans la x, si touche avec la x alors s'arrete obligatoirement.

            #print("vitesse x, pos",self.vitesse_x,self.pos_x) #Pour le débogage
            #print("i",i,i-i%self.base_movement)
            #print("tt",(i-i%self.base_movement+(-self.pos_x*s)%self.base_movement-1)*s)
            
            if i >= self.base_movement:
                i-=self.base_movement

            self.vitesse_x = (i-i%self.base_movement+(-self.pos_x*s)%self.base_movement-1)*s

        elif self.touch_wall(0,(i+1*self.base_movement)*s,grid_cell,cell_dur) :
            if i >= self.base_movement:
                i-=self.base_movement
            #self.pos_y-=1*self.base_movement
            return -1*self.base_movement
        
        return 0

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