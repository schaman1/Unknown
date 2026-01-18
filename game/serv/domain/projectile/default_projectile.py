import time,math
from shared.constants.world import RATIO

class Projectile :

    def __init__(self,pos,life_time,angle,vitesse,id_img,width,height,rebond = False):
        self.pos = pos
        self.life_time = life_time
        self.id=None
        self.spawn_time = time.time()
        self.angle = angle
        self.vitesse = int(vitesse)
        self.id_img = id_img
        self.width = width
        self.height = height
        self.rebond = rebond

        self.is_dead = False
        self.to_update = False

        self.base_movement = RATIO #A changer

        self.vx,self.vy = self.return_vx_vy(angle,vitesse)

    def set_id(self,id):
        self.id = id

    def return_vx_vy(self,angle,vitesse):
        rad = math.radians(angle)
        vx = int(math.cos(rad)*vitesse)
        vy = -int(math.sin(rad)*vitesse)
        return vx,vy

    def move(self,dt,grid_cell,cell_dur):

        self.move_x(dt,grid_cell,cell_dur)
        self.move_y(dt,grid_cell,cell_dur)

    def move_y(self,dt,grid_cell,cell_dur):

        s = self.return_signe(self.vy)
        remaining = int(self.vy*s*dt)

        dist = self.base_movement

        while remaining > 0 :

            for j in range(-self.width//2,self.width//2+1,self.base_movement): #+1 car doit compter le dernier carreau

                if self.touch_wall((self.height//2+self.base_movement)*s,j,grid_cell,cell_dur) :
                    
                    if self.rebond :
                        self.vy=-self.vy
                        s =-s
                        self.angle = (-self.angle)%360
                        self.to_update = True

                    else :
                        self.is_dead = True
                        remaining=0

            if dist < remaining :
                self.pos[1]+=dist*s
            
            else :
                self.pos[1]+= remaining*s

            remaining -= self.base_movement

    def move_x(self,dt,grid_cell,cell_dur):

        s = self.return_signe(self.vx)
        remaining = int(self.vx*s*dt)

        dist = self.base_movement

        while remaining > 0 :

            for j in range(-self.height//2,self.height//2+1,self.base_movement): #+1 car doit compter le dernier

                if self.touch_wall(j,(self.width//2+self.base_movement)*s,grid_cell,cell_dur) :

                    if self.rebond :
                        self.vx=-self.vx
                        s =-s
                        self.angle = (180-self.angle)%360
                        self.to_update = True
                        #self.pos[0]+=dist*s

                    else :
                        self.is_dead = True
                        remaining = 0

            if dist < remaining :
                self.pos[0]+=dist*s
            
            else :
                self.pos[0]+= remaining*s

            remaining -= self.base_movement

    def touch_wall(self,i,j,grid_cell,cell_dur):

        return self.is_type(grid_cell[self.convert_to_base(self.pos[1]+i-self.height//2),self.convert_to_base(self.pos[0]+j)],cell_dur)

    def return_signe(self,el):
        if el <0:
            return -1
        else :
            return 1

    def convert_to_base(self,nbr):
        return nbr//self.base_movement
    
    def should_destroy(self,grid_type,cell_dur):

        if self.is_dead :
            return True
        
        if time.time() - self.spawn_time >= self.life_time :
            return True
    
        else :
            return False
    
    def return_info(self):

        return [self.id,self.pos[0],self.pos[1],self.angle,self.vitesse,self.id_img]
    
    def is_type(self, type_cell, type_check):
        """
        Vérifie si la cellule est du type spécifié.
        ex: type_check = cell_dur (= [2,5]) -> dur si 2 <= type_cell <= 5
        (DÉPLACÉ depuis Skeleton pour que tous les monstres puissent l'utiliser)
        """
        if type_check[0] <= type_cell <= type_check[1]:
           return True
        return False