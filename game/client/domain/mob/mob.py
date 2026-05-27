from shared.constants import world,fps
from client.domain.mob.mob_animation import Animation
import time

class Mob:

    def __init__(self, x,y,cell_size,size,name = "player"):

        self.base_movement = world.RATIO
        self.pos_x = self.convert_from_base(x*cell_size)
        self.pos_y = self.convert_from_base(y*cell_size)
        self.is_looking = 0 #0 = right / 1 = Top / 2 left / 3 bottom
        self.between_pos_x = 0
        self.between_pos_y = 0
        self.cell_size = cell_size
        self.width,self.height = size
        self.pos_blit=0

        self.interpolate_mov = []  #x,y,time
        self.delay = 0.12#1/fps.FPS_SEND_POS_CLIENT
        
        self.life = 100
        self.max_life = 1

        self.animation = Animation(name,cell_size,size[0],size[1])

    def update_pos_blit(self,x,y):
        self.pos_blit = self.calculate_pos_blit(x,y)

    def calculate_pos_blit(self,x,y):
        xs = self.pos_x - self.width//2*self.cell_size +x
        ys = self.pos_y - self.height//2*self.cell_size +y #Regle un petit soucis
        return (xs,ys)
    
    def convert_from_base(self,nbr):
        return nbr//self.base_movement
    
    def update_life(self,amount,max_life):

        if amount!=self.life :

            self.animation.update_color(self.life-amount)
            self.life = amount

            self.text_life = self.font.render(f"{self.life}/{self.max_life}",True, self.text_life_color)  # True = anti-aliasing
        
        self.update_max_life(max_life)

    def update_max_life(self,amount):
        self.max_life = amount
        self.text_life = self.font.render(f"{self.life}/{self.max_life}",True, self.text_life_color)  # True = anti-aliasing

    def update_interpolate_pos(self):
        time_now = time.perf_counter() - self.delay

        if len(self.interpolate_mov) < 2:
            return

        while len(self.interpolate_mov) > 2 and time_now > self.interpolate_mov[1][2]:
            self.interpolate_mov.pop(0)

        x0, y0, t0 = self.interpolate_mov[0]
        x1, y1, t1 = self.interpolate_mov[1]

        div = t1 - t0

        if div <= 0:
            return

        alpha = (time_now - t0) / div

        if alpha < 0:
            alpha = 0

        if alpha <= 1.0:
            pass #No issue more with the camera
            self.pos_x = round((1 - alpha) * x0 + alpha * x1)
            self.pos_y = round((1 - alpha) * y0 + alpha * y1)

        else:
            # Extrapolation limitée
            max_extrapolation = 0.01  # 100 ms max
            dt = min(time_now - t1, max_extrapolation)

            vx = (x1 - x0) / div
            vy = (y1 - y0) / div

            self.pos_x = round(x1 + vx * dt)
            self.pos_y = round(y1 + vy * dt)

    #def update_interpolate_pos(self):
        #
        #time_now = time.perf_counter()-self.delay
#
        #l = len(self.interpolate_mov)
#
        #if l<=1:
        #    return
        #
        #while l>2 and time_now > self.interpolate_mov[1][2] :
        #    l-=1
        #    self.interpolate_mov.pop(0)
#
        #div = self.interpolate_mov[1][2]-self.interpolate_mov[0][2]
#
        #if div == 0:
        #    return
        #if div < time_now-self.interpolate_mov[0][2]:
        #    div = time_now-self.interpolate_mov[0][2]
        #
        #alpha = (time_now-self.interpolate_mov[0][2])/(div)
#
        ##alpha = 1
#
#
        #self.pos_x = round((1-alpha)*self.interpolate_mov[0][0] + (alpha*self.interpolate_mov[1][0]))
        #self.pos_y = round((1-alpha)*self.interpolate_mov[0][1] + (alpha*self.interpolate_mov[1][1]))

    def move_mob(self,new_pos):

        #new_pos = self.convert_from_base(delta[0]*self.cell_size),self.convert_from_base(delta[1]*self.cell_size)

        self.interpolate_mov.append((new_pos[0],new_pos[1],time.perf_counter()))

    def in_dead_state(self):

        return self.animation.dead_state()