from shared.constants import world

class Mob:

    def __init__(self,pos,hp = 100,id=None,width=5,height=5):
        self.pos_x = pos[0]
        self.pos_y = pos[1]

        self.screen_global_size = world.BG_SIZE_SERVER

        self.base_movement = world.RATIO #C'est le mouv de base = si ajoute 100, se deplace de 1 carre plus vite
        
        self.acceleration = 1
        self.gravity_power = 200
        self.acceleration_x = 500
        self.acceleration_y = 80 * self.base_movement
        self.vitesse_x = 0
        self.vitesse_y = 0
        
        self.width = (width-2)*self.base_movement
        self.half_width = self.width//2
        self.height = height*self.base_movement
        self.half_height = self.height//2

        self.life = hp
        self.max_life = hp
        self.send_new_life = False
        self.id = id

    def send_life(self):
        self.send_new_life = False
        return self.life

    def convert_to_base(self,nbr):
        """Retourne le nbr en 100 pour 1"""
        return nbr//self.base_movement
    
    def convert_from_base(self,nbr):
        """Retourne le nbr en 1 pour 100"""
        return nbr*self.base_movement

    def gravity_effect(self):

        #return

        if self.vitesse_y < 500*self.base_movement:
            self.vitesse_y += self.acceleration*self.gravity_power

    def collision_y(self,map,dt):

        #self.pos_y+=self.vitesse_y
        #return

        pos_before = self.pos_y

        s = self.return_signe(self.vitesse_y)
        remaining = int(self.vitesse_y*s*dt)

        while remaining > 0 :

            dist = self.base_movement

            for j in range(-self.half_width,self.half_width+1,self.base_movement): #+1 car doit compter le dernier carreau

                if self.touch_wall((self.half_height+self.base_movement)*s,j,map) :

                    dist = self.base_movement - ((self.pos_y)*s)%self.base_movement -1 #-j*s
                    #if dist!=0:
                    #    print(self.touch_wall(0,0,map),self.touch_wall(dist*s,0,map))
                    #    print("Collisiony",dist*s,remaining*s,self.pos_x,self.pos_y)

                    if dist < remaining :
                        self.vitesse_y = 0

            #if self.vitesse_y != 10 : #pour les testes
            #    print("dist, rem",dist,remaining)
            #    print("pos",self.pos_y,self.vitesse_y)

            if dist < remaining :
                self.pos_y+=dist*s
                remaining=0
            
            else :
                self.pos_y+= remaining*s

            remaining -= self.base_movement

        return self.pos_y - pos_before

    def collision_x(self,map,dt):

        #self.pos_x+=self.vitesse_x
        #return
        
        pos_before = self.pos_x

        s = self.return_signe(self.vitesse_x)
        remaining = int(self.vitesse_x*s*dt)

        while remaining > 0 :

            dist = self.base_movement
            for j in range(-self.half_height,self.half_height+1,self.base_movement): #+1 car doit compter le dernier

                if self.touch_wall(j,(self.half_width+self.base_movement)*s,map) :

                    dist = (self.base_movement - ((self.pos_x+self.half_width)*s)%self.base_movement -1) #-j*s

                    #if dist!=0:
                    #    print(self.touch_wall(0,0,map),self.touch_wall(0,dist*s,map))
                    #    print("Collisionx",dist*s,remaining*s,self.pos_y,self.pos_x)

                    if dist < remaining :
                        #print("Yes !")
                     
                        self.vitesse_x = 0
                    #print()
                    #print("pos_x",self.pos_x)
                    #print(- (self.pos_x*s)%self.base_movement )

            if dist < remaining :
                self.pos_x+=dist*s
                remaining=0
            
            else :
                self.pos_x+= remaining*s

            remaining -= self.base_movement

        return self.pos_x-pos_before
        
    def touch_wall(self,i,j,map):
        return self.is_type(map.return_type(self.convert_to_base(self.pos_y+i-self.half_height),self.convert_to_base(self.pos_x+j)),map.dur)
    
    def touch_ground(self,map):
        j = -self.half_width

        while j<self.half_width+1 and not self.touch_wall(self.half_height+self.base_movement,j,map) :
            j+=self.base_movement

        if j>self.half_width :
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
        
    def return_pos(self):
        return [self.pos_x,self.pos_y]
    
    def take_damage(self,damage):
        self.hp-=damage