import time

class Shoot :

    def __init__(self,pos,life_time,id,angle,vitesse):
        self.pos = pos
        self.life_time = life_time
        self.id=id
        self.spawn_time = time.time()

        self.vx,self.vy = self.return_vx_vy(angle,vitesse)

    def return_vx_vy(self,angle,vitesse):
        return (0*vitesse,0*vitesse)

    def move(self,dt):

        self.pos[0]+=self.vx
        self.pos[1]+=self.vy

        return self.should_destroy()

    def should_destroy(self):

        return time.time() - self.spawn_time >= self.life_time