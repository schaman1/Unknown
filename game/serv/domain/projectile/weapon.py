from serv.domain.projectile.default_projectile import Projectile
from serv.config import weapons

class Pioche(Projectile) :

    def __init__(self,id,angle,pos):

        self.life_time = weapons.LIFE_PIOCHE

        super().__init__(pos,self.life_time,id,angle,vitesse = weapons.V_PIOCHE,id_img = 0)