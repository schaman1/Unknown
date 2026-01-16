from serv.domain.projectile.default_projectile import Projectile
from serv.config import weapons

class Fireball(Projectile) :

    def __init__(self,angle,pos,speed_mult):

        self.life_time = weapons.LIFE_FIREBALL

        super().__init__(pos,self.life_time,angle,vitesse = weapons.V_FIREBALL*speed_mult,id_img = 0)