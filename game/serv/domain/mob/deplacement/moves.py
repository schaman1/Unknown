from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any

class Movable:

    # Type hints to satisfy linters since these attributes are injected by subclasses
    base_movement: int
    vitesse_x: float
    vitesse_y: float
    pos_x: float
    pos_y: float
    half_width: int
    half_height: int
    acceleration: float
    acceleration_x: float
    acceleration_y: float
    screen_global_size: tuple[int, int]
    is_climbing: bool = True
    in_dash:bool=False

    def convert_to_base(self,nbr):
        """Retourne le nbr en 100 pour 1"""
        return nbr//self.base_movement
    
    def convert_from_base(self,nbr):
        """Retourne le nbr en 1 pour 100"""
        return nbr*self.base_movement

    def gravity_effect(self,dt):
        """Update vitesse_y according to gravity physics"""

        #if self.in_dash==True : #Pas de gravité quand est dans un dash
        #    return

        self.vitesse_y += self.base_movement*2*self.acceleration*dt
        s=self.return_signe(self.vitesse_y)

        gravity_power_mult = 1#Diff car dans les game grav plus forte quand tu tombe pour meilleur feeling

        if self.vitesse_y<0:
            gravity_power_mult-=0.1
        else :
            gravity_power_mult+=0.25

        #delta = self.vitesse_y*gravity_power_mult - self.vitesse_y
        #print(dt)
        #delta = delta**(dt)

        self.vitesse_y = self.vitesse_y*(gravity_power_mult**(dt*60))

        #self.vitesse_y += delta

        if self.vitesse_y>self.base_movement*100:
            self.vitesse_y = self.base_movement*100
        #print(self.vitesse_y)

    def collision_y(self,map,dt,vy):

        if self.is_climbing and self.vitesse_y > 0:

            type = map.dur_and_can_climb

        else :
            type = map.dur

        s = self.return_signe(vy)
        remaining = int(vy*s*dt)

        while remaining > 0 :

            #print("remaining",remaining)

            dist = self.base_movement

            for j in range(-self.half_width,self.half_width+1,self.base_movement): #+1 car doit compter le dernier carreau

                if self.touch_type((self.half_height+self.base_movement)*s,j,map,type) :

                    dist = self.base_movement - ((self.pos_y)*s)%self.base_movement -1 #-j*s

                    if dist < remaining :
                        self.vitesse_y = 0

            if dist > remaining :
                self.pos_y+=remaining*s
                remaining = 0
            
            else :
                self.pos_y+= dist*s
                #remaining=0

            remaining -= self.base_movement

        #self.go_up_while_touch_strong(map)

    #def go_up_while_touch_strong(self,map):
    #    while self.touch_type(-(self.half_height+self.base_movement),0,map,map.cannot_be_inside) :
    #        self.pos_y-=self.base_movement

        #return self.pos_y - pos_before

    def collision_x(self,map,dt,vx):

        type = map.dur

        s = self.return_signe(vx)
        remaining = int(vx*s*dt)

        while remaining > 0 :

            dist = self.base_movement
            for j in range(-self.half_height,self.half_height+1,self.base_movement): #+1 car doit compter le dernier

                if self.touch_type(j,(self.half_width+self.base_movement)*s,map,type) :

                    dist = (self.base_movement - ((self.pos_x+self.half_width)*s)%self.base_movement -1) #-j*s

                    if dist < remaining :
                     
                        self.vitesse_x = 0

            if dist > remaining :
                self.pos_x+=remaining*s
                remaining=0
            
            else :
                self.pos_x+= dist*s

            remaining -= self.base_movement

        #return self.pos_x-pos_before

    def touch_type(self,i,j,map,type):
        #print(self.pos_y,i,self.half_height,self.pos_x,j)
        return self.is_type(map.return_type(self.convert_to_base(self.pos_y+i),self.convert_to_base(self.pos_x+j)),type)

    def touch_ground(self,map):
        j = -self.half_width

        while j<self.half_width+1 and not self.touch_type(self.half_height+1,j,map,map.dur_and_can_climb) : #Plus 1 car on est tj à x * 100 + 99 = doit ajouter 1 pout voir le sol
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

        #print(e)
        if e<0:
            return -1
        else :
            return 1
            
    # From Monster
    
    def is_blocking_cell(self, cell_type, cell_dur, cell_liquid):
        return self.is_type(cell_type, cell_dur) or self.is_type(cell_type, cell_liquid)

    def try_move_axis_x(self, dx, cells_arr, cell_dur, cell_liquid):
        if dx == 0:
            return 0

        s = -1 if dx < 0 else 1
        remaining = abs(dx)
        moved = 0

        while remaining > 0:
            step = min(self.base_movement, remaining)
            next_x = self.pos_x + s * step

            x_check = next_x + (self.half_width + self.base_movement) * s
            y_top = self.pos_y - self.half_height
            y_bottom = self.pos_y + self.half_height

            ok = True
            y = y_top
            while y <= y_bottom:
                bx = self.convert_to_base(x_check)
                by = self.convert_to_base(y)

                if by < 0 or by >= cells_arr.shape[0] or bx < 0 or bx >= cells_arr.shape[1]:
                    ok = False
                    break

                if self.is_blocking_cell(int(cells_arr[by, bx]), cell_dur, cell_liquid):
                    ok = False
                    break

                y += self.base_movement

            if not ok:
                break

            self.pos_x = next_x
            moved += s * step
            remaining -= step

        return moved

    def try_move_axis_y(self, dy, cells_arr, cell_dur, cell_liquid):
        if dy == 0:
            return 0

        s = -1 if dy < 0 else 1
        remaining = abs(dy)
        moved = 0

        while remaining > 0:
            step = min(self.base_movement, remaining)
            next_y = self.pos_y + s * step

            y_check = next_y + (self.half_height + self.base_movement) * s
            x_left = self.pos_x - self.half_width
            x_right = self.pos_x + self.half_width

            ok = True
            x = x_left
            while x <= x_right:
                bx = self.convert_to_base(x)
                by = self.convert_to_base(y_check)

                if by < 0 or by >= cells_arr.shape[0] or bx < 0 or bx >= cells_arr.shape[1]:
                    ok = False
                    break

                if self.is_blocking_cell(int(cells_arr[by, bx]), cell_dur, cell_liquid):
                    ok = False
                    break

                x += self.base_movement

            if not ok:
                break

            self.pos_y = next_y
            moved += s * step
            remaining -= step

        return moved
    
    def overlaps_dur(self,map):
        i = -self.half_height
        while i <= self.half_height:
            j = -self.half_width
            while j <= self.half_width:
                if self.touch_type(i, j,map,map.dur):
                    return True
                j += self.base_movement
            i += self.base_movement
        return False

    def try_step_up_1(self,map, intended_vx,dt):
        if intended_vx == 0:
            return 0

        if not self.touch_ground(map):
            return 0

        old_x = self.pos_x
        old_y = self.pos_y
        old_vx = self.vitesse_x

        self.pos_y = old_y - self.base_movement
        if self.overlaps_dur(map):
            self.pos_x = old_x
            self.pos_y = old_y
            self.vitesse_x = old_vx
            return 0
        self.vitesse_x = intended_vx
        moved = self.collision_x(map,dt,self.vitesse_x)

        if moved == 0:
            self.pos_x = old_x
            self.pos_y = old_y
            self.vitesse_x = old_vx
            return 0
        return moved
    
    def can_climb(self,map):
        return self.touch_element(map,element = map.can_climb)

    def touch_element(self, map,element):

        j = self.half_width+1
        i = -self.half_height

        while i < self.half_height+1 and j > self.half_width :
    
            j = -self.half_width

            while j<self.half_width+1 and not self.touch_type(i,j,map,element) : #Plus 1 car on est tj à x * 100 + 99 = doit ajouter 1 pout voir le sol
                j+=self.base_movement

            i+=self.base_movement

        if i > self.half_height :
            return False
    
        else :
            return True

    def climb(self, map, direction, dt):
        #direction: -1 for UP, 1 for DOWN
        if self.can_climb(map):
            self.is_climbing = True
            
            speed = self.base_movement * 40 # Climbing speed (similar to max speed)
            self.vitesse_y = direction * speed
            
            # Predict movement
            new_y = self.pos_y + self.vitesse_y * dt
            
            # Check bounds/collision if needed, but for now simple movement
            # Validate if new position is still on ladder? 
            # If we move OFF the ladder, we should probably stop climbing or fall
            
            # For simplicity, move first
            pos_before = self.pos_y
            self.pos_y = new_y
            
            if not self.can_climb(map):
                # If we moved off the ladder
                # If going UP, we might have reached the top.
                # If going DOWN, we might have reached the bottom.
                pass
            
        else:
            self.is_climbing = False

    def dash(self,v):
        """Now dash update the speed"""

        #if self.vitesse_y<0 : #Test pour améliorer le feeling
        #    self.vitesse_y = 0

        if v[0]!=0 :
            self.vitesse_x = v[0]
        if v[1]!=0 :
            self.vitesse_y = v[1]

    def stop_dash(self):

        self.in_dash = False

    def start_dash(self):
        self.in_dash = True