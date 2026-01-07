import time

class Projectile :

    def __init__(self,pos,life_time,id,angle,vitesse,id_img):
        self.pos = pos
        self.life_time = life_time
        self.id=id
        self.spawn_time = time.time()
        self.angle = angle
        self.vitesse = vitesse
        self.id_img = id_img

        self.vx,self.vy = self.return_vx_vy(angle,vitesse)

    def return_vx_vy(self,angle,vitesse):
        return (0*vitesse,0*vitesse)

    def move(self,dt):

        self.pos[0]+=self.vx*dt
        self.pos[1]+=self.vy*dt

    def should_destroy(self):

        return time.time() - self.spawn_time >= self.life_time
    
    def return_info(self):
        return [self.id,self.pos[0],self.pos[1],self.vitesse,self.angle,self.id_img]