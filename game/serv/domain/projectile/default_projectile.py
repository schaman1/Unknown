import time
from shared.constants.world import RATIO

class Projectile :

    def __init__(self,pos,life_time,id,angle,vitesse,id_img):
        self.pos = pos
        self.life_time = life_time
        self.id=id
        self.spawn_time = time.time()
        self.angle = angle
        self.vitesse = vitesse
        self.id_img = id_img

        self.base_movement = RATIO #A changer

        self.vx,self.vy = self.return_vx_vy(angle,vitesse)

    def return_vx_vy(self,angle,vitesse):
        return (1*vitesse,0*vitesse)

    def move(self,dt):

        self.pos[0]+=int(self.vx*dt)
        self.pos[1]+=int(self.vy*dt)

    def convert_to_base(self,nbr):
        return nbr//self.base_movement
    
    def touch_wall(self,i,j,grid_type,cell_dur):

        return self.is_type(
            grid_type[
                self.convert_to_base(self.pos[1]+i),
                self.convert_to_base(self.pos[0]+j)
                ],
            cell_dur)

    def should_destroy(self,grid_type,cell_dur):

        if self.touch_wall(0,0,grid_type,cell_dur) :
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