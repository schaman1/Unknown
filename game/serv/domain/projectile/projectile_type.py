from serv.domain.projectile.default_projectile import Projectile
from serv.config import weapons

class Fire(Projectile) :

    def __init__(self,angle,pos,team,randomize,owner):

        self.life_time = weapons.LIFE_FIRE

        super().__init__(pos,self.life_time,angle,
                         speed = weapons.V_FIRE,
                         id_img = 2,
                         width = weapons.WIDTH_FIRE,
                         height = weapons.HEIGHT_FIRE,
                         rebond = weapons.REBOND_FIRE,
                         damage = weapons.DAMAGE_FIRE,
                         team=team,
                         randomize_angle=randomize,
                         owner_pos=owner)
        
class Magic(Projectile) :

    def __init__(self,angle,pos,team,randomize,owner):

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
                         randomize_angle=randomize,
                         owner_pos=owner)
        
class Lune(Projectile) :

    def __init__(self,angle,pos,team,randomize,owner):

        self.life_time = weapons.LUNE_LIFE

        super().__init__(pos,self.life_time,angle,
                         speed = weapons.LUNE_V,
                         id_img = 3,
                         width = weapons.LUNE_WIDTH,
                         height = weapons.LUNE_HEIGHT,
                         damage = weapons.LUNE_DAMAGE,
                         team=team,
                         randomize_angle=randomize,
                         owner_pos=owner)
        
class Laser(Projectile) :

    def __init__(self,angle,pos,team,randomize,owner):

        self.life_time = weapons.LASER_LIFE

        super().__init__(pos,self.life_time,angle,
                         speed = weapons.LASER_V,
                         id_img = 5,
                         width = weapons.LASER_WIDTH,
                         height = weapons.LASER_HEIGHT,
                         damage = weapons.LASER_DAMAGE,
                         team=team,
                         randomize_angle=randomize,
                         owner_pos=owner)
        
class Pompe(Projectile) :

    def __init__(self,angle,pos,team,randomize,owner):

        self.life_time = weapons.POMPE_LIFE

        super().__init__(pos,self.life_time,angle,
                         speed = weapons.POMPE_V,
                         id_img = 4,
                         width = weapons.POMPE_WIDTH,
                         height = weapons.POMPE_HEIGHT,
                         damage = weapons.POMPE_DAMAGE,
                         team=team,
                         randomize_angle=randomize,
                         owner_pos=owner)
        
class Stone(Projectile) :

    def __init__(self,angle,pos,team,randomize,owner):

        self.life_time = weapons.STONE_LIFE

        super().__init__(pos,self.life_time,angle,
                         speed = weapons.STONE_V,
                         id_img = 7,
                         width = weapons.STONE_WIDTH,
                         height = weapons.STONE_HEIGHT,
                         damage = weapons.STONE_DAMAGE,
                         weight = weapons.STONE_WEIGHT,
                         team=team,
                         randomize_angle=randomize,
                         owner_pos=owner)