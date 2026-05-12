import time,math
from shared.constants.world import RATIO
from serv.domain.mob.team import Team

class Projectile :

    def __init__(self,pos,life_time,angle,speed,id_img,width,height,rebond = False,damage = 0,weight = 0,team = Team.Mob):
        self.pos_x,self.pos_y = pos
        self.projectile_spawn_when_die = []
        self.life_time = life_time
        self.id=None
        self.spawn_time = time.time()
        self.angle = angle
        self.speed = int(speed)
        self.id_img = id_img
        self.width = width
        self.half_width = self.width//2
        self.height = height
        self.half_height = self.height//2
        self.rebond = rebond
        self.damage = damage

        self.is_dead = False
        self.to_update = False
        self.team = team

        self.base_movement = RATIO 
        self.weight = weight*self.base_movement

        self.owner = None

    def update_angle_pos(self,new_angle,new_pos):
        self.pos_x,self.pos_y=new_pos
        self.angle=new_angle
        print("Created with value : ",self.angle,self.vx,self.pos_x,self.pos_y)
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
            projectile.update_angle_pos(self.angle,[self.pos_x,self.pos_y])
        return self.projectile_spawn_when_die

    def move(self,dt,map):

        #self.gravity(dt)

        if (self.pos_x+self.vx*dt<0 or self.pos_y+self.vy < 0):
            self.is_dead = True

    # je t'aime

        if self.is_dead is False:
            self.move_x(map,dt)

        if self.is_dead is False:
            self.move_y(map,dt)

#    def complete_mov_x(self,s,deltax,complete_mov_to_touch_wall):
#        #print("before x : ",self.pos,self.id)
#
#        self.pos_x+=complete_mov_to_touch_wall
#
#        self.pos_y+=((complete_mov_to_touch_wall+deltax)/self.vx)*self.vy#*(self.return_signe(self.pos_y))
#        #print(self.pos)
#
#    def complete_mov_y(self,s,rest_y_to_complete_mouv,complete_mov_to_touch_wall):
#        #print("before y : ",self.pos,self.id)
#        self.pos_y += complete_mov_to_touch_wall
#
#        self.pos_x-=(rest_y_to_complete_mouv-complete_mov_to_touch_wall)/self.vy*self.vx#*(self.return_signe(self.pos_x))
#        #print(self.pos)
#
#    def move_y(self,dt,map):
#
#        s = self.return_signe(self.vy)
#        remaining = self.vy*s*dt
#        old_pos = self.pos_y
#
#        dist = self.base_movement
#
#        tmp_death = False
#
#        while remaining > 0 :
#
#            for j in range(0,(self.base_movement+1)*s,self.base_movement*s): #+1 car doit compter le dernier
#
#                if tmp_death is False and self.touch_wall(j,0,map) :
#                    
#                    rest_y_to_complete_mouv = self.vy*dt - (self.pos_y-old_pos)
#
#                    complete_mov_to_touch_wall = (self.base_movement - (self.pos_y*s)%self.base_movement)*s
#                    if complete_mov_to_touch_wall*s<=remaining :
#
#                        self.complete_mov_y(s,rest_y_to_complete_mouv,complete_mov_to_touch_wall)
#
#                        #Rebond en y
#                        self.vy=-self.vy
#                        #s =-s
#                        self.angle = (180-self.angle)%360
#                        #Complete la dist pr toucher le mur
#                        #print("Die on y")
#                        tmp_death = True
#
#            if tmp_death :
#                if self.rebond :
#                    self.to_update = True
#                    remaining = 0
#
#                else :
#                    self.is_dead = True
#                    remaining=0
#
#            if dist < remaining :
#                self.pos_y+=dist*s
#                remaining -= self.base_movement
#
#            else :
#                self.pos_y+= remaining*s
#                remaining -= self.base_movement
#
#            #if self.is_dead:
#            #    print(self.pos_y)
#
#    def move_x(self,dt,map):
#
#        s = self.return_signe(self.vx)
#        old_pos = self.pos_x
#        remaining = self.vx*s*dt
#
#        #self.pos_x+=remaining*s
#        #return
#
#        dist = self.base_movement
#
#        tmp_death = False
#
#        while remaining > 0 :
#
#            for j in range(0,(self.base_movement+1)*s,self.base_movement*s): #+1 car doit compter le dernier
#
#                if tmp_death is False and self.touch_wall(0,j,map) :
#
#                    #Complete la dist
#
#                    complete_mov_to_touch_wall = (self.base_movement - (self.pos_x*s)%self.base_movement)*s
#
#                    if complete_mov_to_touch_wall*s<=remaining :
#
#                        deltax = (self.pos_x-old_pos)
#
#                        #print("Remaining :",remaining,self.vx*s*dt,j)
#                        #print("Before : ",self.angle,self.vx,self.pos_x,self.pos_y)
#                        self.complete_mov_x(s,deltax,complete_mov_to_touch_wall)
#                        #print("After : ",self.pos_x,self.pos_y)
#
#                        #Rebond en x
#                        self.vx=-self.vx
#                        #s =-s
#                        self.angle = (-self.angle)%360 #Rotate the spell
#
#                        #print("old x : ",self.pos_x)
#                        #print("New x :",self.pos_x+dist*s)
#                        #print("normal : ",self.pos_x+dist*s)
#
#                        tmp_death = True
#                        
#            if tmp_death is True:
#
#                if self.rebond :
#                    
#                    self.to_update = True
#                    remaining = 0
#
#                    #self.pos_x+=dist*s
#
#                else :
#                    self.is_dead = True
#                    remaining = 0
#
#            elif dist < remaining :
#                self.pos_x+=dist*s
#                remaining -= self.base_movement
#            
#            else :
#                self.pos_x+= remaining*s
#                remaining -= self.base_movement

    #def touch_wall(self,i,j,map):
    #    return self.is_type(map.return_type(self.convert_to_base(self.pos_y+i),self.convert_to_base(self.pos_x+j)),map.dur)
    
    def move_y(self,map,dt):

        vy = self.vy

        type = map.dur

        s = self.return_signe(vy)
        remaining = int(vy*s*dt)

        touch_wall = False

        while remaining > 0 and touch_wall is False:

            #print("remaining",remaining)

            dist = self.base_movement

            for j in range(-self.half_width,self.half_width+1,self.base_movement): #+1 car doit compter le dernier carreau

                if self.touch_type((self.half_height+self.base_movement)*s,j,map,type) :

                    dist = self.base_movement - ((self.pos_y)*s)%self.base_movement -1 #-j*s

                    if dist <= remaining :
                        touch_wall = True

                        if self.rebond :
                            self.to_update = True
                        else :
                            self.is_dead = True

                        self.angle = (-self.angle)%360
                        self.vy = -self.vy

                    break

            if dist > remaining :
                self.pos_y+=remaining*s
                remaining = 0
            
            else :
                self.pos_y+= dist*s
                #remaining=0

            remaining -= self.base_movement

    def move_x(self,map,dt):

        vx = self.vx

        type = map.dur

        s = self.return_signe(vx)
        remaining = int(vx*s*dt)

        touch_wall = False

        while remaining > 0  and touch_wall is False:

            dist = self.base_movement
            for j in range(-self.half_height,self.half_height+1,self.base_movement): #+1 car doit compter le dernier

                if self.touch_type(j,(self.half_width+self.base_movement)*s,map,type) :

                    dist = (self.base_movement - ((self.pos_x+self.half_width)*s)%self.base_movement -1) #-j*s
                    
                    if dist <= remaining :

                        #Death update
                        touch_wall = True

                        #print("Die with value :",self.pos_x+dist*s,self.angle,self.vx,j)

                        if self.rebond :
                            self.to_update = True
                        else :
                            self.is_dead = True

                        self.angle = (180-self.angle)%360
                        self.vx = -self.vx

                    break

            if dist > remaining :
                self.pos_x+=remaining*s
                remaining=0
            
            else :
                self.pos_x+= dist*s

            remaining -= self.base_movement

    def touch_type(self,i,j,map,type):
        #print(self.pos_y,i,self.half_height,self.pos_x,j)
        return self.is_type(map.return_type(self.convert_to_base(self.pos_y+i),self.convert_to_base(self.pos_x+j)),type)

    def is_type(self, type_cell, type_check):
        """Vérifie si la cellule à la position (x,y) est du type spécifié"""
        if type_check[0] <= type_cell <= type_check[1]:
            return True
        return False

    def return_signe(self,el):
        if el <0:
            return -1
        else :
            return 1

    def convert_to_base(self,nbr):
        return int(nbr//self.base_movement)
    
    def should_destroy(self,map):

        if self.is_dead :
            return True
        
        if time.time() - self.spawn_time >= self.life_time :
            return True
    
        else :
            return False
    
    def return_info(self):

        return [self.id,int(self.pos_x),int(self.pos_y),self.angle,self.speed,self.weight//self.base_movement,self.id_img]
    
    def is_type(self, type_cell, type_check):
        """
        Vérifie si la cellule est du type spécifié.
        ex: type_check = cell_dur (= [2,5]) -> dur si 2 <= type_cell <= 5
        (DÉPLACÉ depuis Skeleton pour que tous les monstres puissent l'utiliser)
        """
        if type_check[0] <= type_cell <= type_check[1]:
           return True
        return False