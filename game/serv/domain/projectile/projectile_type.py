from serv.domain.projectile.default_projectile import Projectile
from serv.config import weapons

class Fire(Projectile) :

    def __init__(self,angle,pos):

        self.life_time = weapons.LIFE_FIRE

        super().__init__(pos,self.life_time,angle,
                         speed = weapons.V_FIRE,
                         id_img = 2,
                         width = weapons.WIDTH_FIRE,
                         height = weapons.HEIGHT_FIRE,
                         rebond = weapons.REBOND_FIRE,
                         damage = weapons.DAMAGE_FIRE,
                         weight = weapons.WEIGHT_FIRE)
        
class Magic(Projectile) :

    def __init__(self,angle,pos):

        self.life_time = weapons.LIFE_MAGIC

        super().__init__(pos,self.life_time,angle,
                         speed = weapons.V_MAGIC,
                         id_img = 0,
                         width = weapons.WIDTH_MAGIC,
                         height = weapons.HEIGHT_MAGIC,
                         rebond = weapons.REBOND_MAGIC,
                         damage = weapons.DAMAGE_MAGIC,
                         weight = weapons.WEIGHT_MAGIC)