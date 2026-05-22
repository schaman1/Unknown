from client.domain.projectile.default_projectile import DefaultProjectile
from client.domain.projectile.default_explosion import DefaultExplosion
from shared.constants.fps import FPS_UPDATE_POS_PROJ

class ProjectileManager :

    def __init__(self,cell_size):

        self.d_Projectile = {}
        self.explosion = []
        self.cell_size = cell_size

        self.accumulator = 0

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

        sould_move = self.should_move(dt)

        for projectile in self.d_Projectile.values():

            if sould_move :
                projectile.move(FPS_UPDATE_POS_PROJ)

            projectile.blit(screen,x,y)

        for i in range(len(self.explosion)-1,-1,-1):

            self.explosion[i].blit(screen,x,y)            

            if self.explosion[i].die() :

                self.explosion.pop(i)

    def should_move(self,dt):

        self.accumulator +=dt
        if self.accumulator>=FPS_UPDATE_POS_PROJ :
            self.accumulator -= FPS_UPDATE_POS_PROJ
            return True
        
        return False