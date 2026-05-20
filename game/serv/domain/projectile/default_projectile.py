import time,math,random
from shared.constants.world import RATIO
from serv.domain.mob.team import Team

class Projectile :

    def __init__(self,pos,life_time,angle,speed,id_img,width,height,rebond = False,damage = 0,weight = 0,team = Team.Mob,randomize_angle = False,owner_pos = None,knockback = 0):
        self.pos_x,self.pos_y = pos
        self.owner_pos = owner_pos #Use to set default pos

        self.projectile_spawn_when_die = []
        self.life_time = life_time
        self.id=None
        self.spawn_time = time.time()

        self.randomize_angle = randomize_angle
        self.delta_angle = 0

        self.force_angle = False
        self.force_pos = False
        self.delta_pos = [0,0]
        self.angle_force = 0

        if self.randomize_angle :
            self.angle = random.randint(1,360)
        else :
            self.angle = angle

        self.speed = int(speed)
        self.id_img = id_img
        self.width = width
        self.half_width = self.width//2
        self.height = height
        self.half_height = self.height//2
        self.rebond = rebond
        self.damage = damage
        self.knockback = knockback #Knockback strength applied to mobs on hit (0 = none)

        self.is_dead = False
        self.to_update = False
        self.team = team

        self.base_movement = RATIO 
        self.weight = weight

        self.owner = None

    def update_angle_pos(self,new_angle,new_pos,owner_pos):

        #print(self.force_pos,new_pos,self.delta_pos)

        if self.force_pos :
            self.pos_x = new_pos[0]+self.delta_pos[0]
            self.pos_y = new_pos[1]+self.delta_pos[1]

        else :
            self.pos_x,self.pos_y=new_pos

        if self.randomize_angle :
            self.angle = random.randint(1,360)

        elif self.force_angle :
            self.angle = self.angle_force
            
        else :
            self.angle = (new_angle+self.delta_angle)%360

        self.spawn_time = time.time()

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

    # je t'aime
        self.vy += self.base_movement*self.weight*dt

        gravity_power_mult = 1.1#Diff car dans les game grav plus forte quand tu tombe pour meilleur feeling

        if self.weight != 0 :
            self.vy = self.vy*(gravity_power_mult**(dt*60))
        pass#self.vy+=self.weight*dt

    def check_if_projectile_spawn_when_die(self):
        for projectile in self.projectile_spawn_when_die :
            projectile.update_angle_pos(self.angle,[self.pos_x,self.pos_y],self.owner_pos)
        return self.projectile_spawn_when_die

    def move(self,dt,map):

        self.gravity(dt)

        if (self.pos_x+self.vx*dt<0 or self.pos_y+self.vy < 0):
            self.is_dead = True

        if self.is_dead is False:
            self.move_x(map,dt)

        if self.is_dead is False:
            self.move_y(map,dt)

    def move_y(self,map,dt):

        vy = self.vy

        type = map.dur_and_can_climb

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

        type = map.dur_and_can_climb

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

        return [self.id,int(self.pos_x),int(self.pos_y),self.angle,self.speed,self.weight,self.id_img]
    
    def is_type(self, type_cell, type_check):
        """
        Vérifie si la cellule est du type spécifié.
        ex: type_check = cell_dur (= [2,5]) -> dur si 2 <= type_cell <= 5
        (DÉPLACÉ depuis Skeleton pour que tous les monstres puissent l'utiliser)
        """
        if type_check[0] <= type_cell <= type_check[1]:
           return True
        return False