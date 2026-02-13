from client.domain.projectile.default_projectile import DefaultProjectile
from client.domain.projectile.default_explosion import DefaultExplosion


class ProjectileManager :

    def __init__(self,cell_size):

        self.d_Projectile = {}
        self.explosion = []
        self.cell_size = cell_size


    def create_projectile(self,id,pos_x,pos_y,angle,vitesse,weight,id_img):

        self.d_Projectile[id] = DefaultProjectile(pos_x,pos_y,angle,vitesse,weight,id_img,self.cell_size)

    def add_explosion(self,pos,projectile,cell_size):

        explosion = DefaultExplosion(pos,projectile,cell_size)
        self.explosion.append(explosion)

    def remove_projectile(self,id,pos_x,pos_y):

        projectile = self.d_Projectile[id]

        self.add_explosion([pos_x,pos_y],projectile,self.cell_size)

        #print(self.d_Projectile[id].pos_x,self.d_Projectile[id].pos_y)
        #self.d_Projectile[id].pos_x = pos_x
        #self.d_Projectile[id].pos_y = pos_y
        #self.d_Projectile[id].vx = 0
        #self.d_Projectile[id].vy = 0

        del self.d_Projectile[id]

    def blit_projectiles_explosions(self,screen,x,y,dt):

        for projectile in self.d_Projectile.values():

            projectile.move(dt)
            projectile.blit(screen,x,y)


        for i in range(len(self.explosion)-1,-1,-1):

            self.explosion[i].blit(screen,x,y)            

            if self.explosion[i].die() :

                self.explosion.pop(i)


