from client.domain.projectile.default_projectile import DefaultProjectile

class ProjectileManager :

    def __init__(self,cell_size):

        self.d_Projectile = {}
        self.cell_size = cell_size

    def create_projectile(self,id,pos_x,pos_y,angle,vitesse,id_img):

        self.d_Projectile[id] = DefaultProjectile(pos_x,pos_y,angle,vitesse,id_img,self.cell_size)

    def remove_projectile(self,id):

        del self.d_Projectile[id]

    def blit_projectiles(self,screen,x,y):

        for projectiles in self.d_Projectile.values():

            projectiles.blit(screen,x,y)