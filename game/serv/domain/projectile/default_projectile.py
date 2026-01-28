import time,math
from shared.constants.world import RATIO

class Projectile :

    def __init__(self,pos,life_time,angle,speed,id_img,width,height,rebond = False,damage = 0,weight = 0):
        self.pos = pos
        self.projectile_spawn_when_die = []
        self.life_time = life_time
        self.id=None
        self.spawn_time = time.time()
        self.angle = angle
        self.speed = int(speed)
        self.id_img = id_img
        self.width = width
        self.height = height
        self.rebond = rebond
        self.damage = damage

        self.is_dead = False
        self.to_update = False

        self.base_movement = RATIO 
        self.weight = weight*self.base_movement

    def update_angle_pos(self,new_angle,new_pos):
        self.pos=new_pos
        self.angle=new_angle
        self.load()

    def load(self):
        self.vx,self.vy = self.return_vx_vy(self.angle,self.speed)

    def set_id(self,id):
        self.id = id

    def return_vx_vy(self,angle,speed):
        rad = math.radians(angle)
        vx = int(math.cos(rad)*speed)
        vy = -int(math.sin(rad)*speed)
        return vx,vy
    
    def gravity(self,dt):
        pass#self.vy+=self.weight*dt

    def check_if_projectile_spawn_when_die(self):
        for projectile in self.projectile_spawn_when_die :
            projectile.update_angle_pos(self.angle,self.pos)
        return self.projectile_spawn_when_die

    def move(self,dt,grid_cell,cell_dur):

        #self.gravity(dt)

    # je t'aime

        if self.is_dead is False:
            self.move_x(dt,grid_cell,cell_dur)

        if self.is_dead is False:
            self.move_y(dt,grid_cell,cell_dur)

    def complete_mov_x(self,s,deltax):
        print("before x : ",self.pos,self.id)
        dist = (self.base_movement - (self.pos[0]*s)%self.base_movement)*s
        self.pos[0]+=dist

        self.pos[1]+=(dist+deltax)/self.vx*self.vy#*(self.return_signe(self.pos[1]))
        print(self.pos)

    def complete_mov_y(self,s,rest_y_to_complete_mouv):
        print("before y : ",self.pos,self.id)
        dist = (self.base_movement - (self.pos[1]*s)%self.base_movement)*s
        self.pos[1] += dist

        self.pos[0]-=(rest_y_to_complete_mouv-dist)/self.vy*self.vx#*(self.return_signe(self.pos[0]))
        print(self.pos)

    def move_y(self,dt,grid_cell,cell_dur):

        s = self.return_signe(self.vy)
        remaining = self.vy*s*dt
        old_pos = self.pos[1]

        dist = self.base_movement

        while remaining > 0 :

            for j in range(0,(self.base_movement+1)*s,self.base_movement*s): #+1 car doit compter le dernier

                if self.is_dead is False and self.touch_wall(j,0,grid_cell,cell_dur) :
                    
                    rest_y_to_complete_mouv = self.vy*dt - (self.pos[1]-old_pos)

                    complete_mov = (self.base_movement - (self.pos[1]*s)%self.base_movement)*s
                    if complete_mov*s<=remaining :

                        self.complete_mov_y(s,rest_y_to_complete_mouv)

                        #Rebond en y
                        self.vy=-self.vy
                        s =-s
                        self.angle = (-self.angle)%360
                        #Complete la dist pr toucher le mur

                        if self.rebond :
                            self.to_update = True

                        else :
                            self.is_dead = True
                            remaining=0

            if dist < remaining :
                self.pos[1]+=dist*s

            else :
                self.pos[1]+= remaining*s

            remaining -= self.base_movement

            #if self.is_dead:
            #    print(self.pos[1])

    def move_x(self,dt,grid_cell,cell_dur):

        s = self.return_signe(self.vx)
        old_pos = self.pos[0]
        remaining = self.vx*s*dt

        #self.pos[0]+=remaining*s
        #return

        dist = self.base_movement

        while remaining > 0 :

            for j in range(0,(self.base_movement+1)*s,self.base_movement*s): #+1 car doit compter le dernier

                if self.is_dead is False and self.touch_wall(0,j,grid_cell,cell_dur) :


                        #Complete la dist

                    complete_mov = (self.base_movement - (self.pos[0]*s)%self.base_movement)*s

                    if complete_mov*s<=remaining :


                        deltax = (self.pos[0]-old_pos)

                        self.complete_mov_x(s,deltax)

                        #Rebond en x
                        self.vx=-self.vx
                        s =-s
                        self.angle = (180-self.angle)%360

                        #print("old x : ",self.pos[0])
                        #print("New x :",self.pos[0]+dist*s)
                        #print("normal : ",self.pos[0]+dist*s)
                        
                        if self.rebond :
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

            #if self.is_dead:
            #    print(self.pos[0])


    def touch_wall(self,i,j,grid_cell,cell_dur):

        #print(self.convert_to_base(self.pos[0]+j),self.convert_to_base(self.pos[1]+i))

        return self.is_type(grid_cell[self.convert_to_base(self.pos[1]+i),self.convert_to_base(self.pos[0]+j)],cell_dur)

    def return_signe(self,el):
        if el <0:
            return -1
        else :
            return 1

    def convert_to_base(self,nbr):
        return int(nbr//self.base_movement)
    
    def should_destroy(self,grid_type,cell_dur):

        if self.is_dead :
            return True
        
        if time.time() - self.spawn_time >= self.life_time :
            return True
    
        else :
            return False
    
    def return_info(self):

        return [self.id,int(self.pos[0]),int(self.pos[1]),self.angle,self.speed,self.weight//self.base_movement,self.id_img]
    
    def is_type(self, type_cell, type_check):
        """
        Vérifie si la cellule est du type spécifié.
        ex: type_check = cell_dur (= [2,5]) -> dur si 2 <= type_cell <= 5
        (DÉPLACÉ depuis Skeleton pour que tous les monstres puissent l'utiliser)
        """
        if type_check[0] <= type_cell <= type_check[1]:
           return True
        return False