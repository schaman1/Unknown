import time

class Shoot :

    def __init__(self,pos,vx,vy,life_time,img,id):
        self.pos = pos
        self.vx,self.vy=vx,vy
        self.life_time = life_time
        self.id=id
        self.spawn_time = time.time()

        self.img = img

    def trigger(self,dt):

        self.pos[0]+=self.vx
        self.pos[1]+=self.vy

        return self.should_destroy()

    def should_destroy(self):

        return time.time() - self.spawn_time >= self.life_time