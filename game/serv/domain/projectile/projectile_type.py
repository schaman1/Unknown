from serv.domain.projectile.default_projectile import Projectile
from serv.config import weapons

class Fire(Projectile) :

    def __init__(self,angle,pos,team,randomize):

        self.life_time = weapons.LIFE_FIRE

        super().__init__(pos,self.life_time,angle,
                         speed = weapons.V_FIRE,
                         id_img = 2,
                         width = weapons.WIDTH_FIRE,
                         height = weapons.HEIGHT_FIRE,
                         rebond = weapons.REBOND_FIRE,
                         damage = weapons.DAMAGE_FIRE,
                         weight = weapons.WEIGHT_FIRE,
                         team=team,
                         randomize_angle=randomize)
        
class Magic(Projectile) :

    def __init__(self,angle,pos,team,randomize):

        self.life_time = weapons.LIFE_MAGIC

        super().__init__(pos,self.life_time,angle,
                         speed = weapons.V_MAGIC,
                         id_img = 1,
                         width = weapons.WIDTH_MAGIC,
                         height = weapons.HEIGHT_MAGIC,
                         rebond = weapons.REBOND_MAGIC,
                         damage = weapons.DAMAGE_MAGIC,
                         weight = weapons.WEIGHT_MAGIC,
                         team=team,
                         randomize_angle=randomize)
        
class Lune(Projectile) :

    def __init__(self,angle,pos,team,randomize):

        self.life_time = weapons.LUNE_LIFE

        super().__init__(pos,self.life_time,angle,
                         speed = weapons.LUNE_V,
                         id_img = 3,
                         width = weapons.LUNE_WIDTH,
                         height = weapons.LUNE_HEIGHT,
                         damage = weapons.LUNE_DAMAGE,
                         team=team,
                         randomize_angle=randomize)
        
class Pompe(Projectile) :

    def __init__(self,angle,pos,team,randomize):

        self.life_time = weapons.POMPE_LIFE

        super().__init__(pos,self.life_time,angle,
                         speed = weapons.POMPE_V,
                         id_img = 4,
                         width = weapons.POMPE_WIDTH,
                         height = weapons.POMPE_HEIGHT,
                         damage = weapons.POMPE_DAMAGE,
                         team=team,
                         randomize_angle=randomize)