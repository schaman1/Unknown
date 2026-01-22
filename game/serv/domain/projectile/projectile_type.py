from serv.domain.projectile.default_projectile import Projectile
from serv.config import weapons

class Fireball(Projectile) :

    def __init__(self,angle,pos):

        self.life_time = weapons.LIFE_FIREBALL

        super().__init__(pos,self.life_time,angle,
                         speed = weapons.V_FIREBALL,
                         id_img = 0,
                         width = weapons.WIDTH_FIREBALL,
                         height = weapons.HEIGHT_FIREBALL,
                         rebond = weapons.REBOND_FIREBALL,
                         damage = weapons.DAMAGE_FIREBALL,
                         weight = weapons.WEIGHT_FIREBALL)