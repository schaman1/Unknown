from serv.domain.projectile.default_projectile import Projectile
from serv.config import weapons
import random

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
                         owner_pos=owner,
                         knockback = weapons.KNOCKBACK_FIRE)
        
class Fire_B(Projectile) :

    def __init__(self,angle,pos,team,randomize,owner):

        self.life_time = weapons.LIFE_FIRE

        super().__init__(pos,self.life_time,angle,
                         speed = weapons.V_FIRE_B,
                         id_img = 47,
                         width = weapons.WIDTH_FIRE_B,
                         height = weapons.HEIGHT_FIRE_B,
                         rebond = weapons.REBOND_FIRE_B,
                         damage = weapons.DAMAGE_FIRE_B,
                         team=team,
                         randomize_angle=randomize,
                         owner_pos=owner,
                         knockback = weapons.KNOCKBACK_FIRE_B)
        
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
                         owner_pos=owner,
                         knockback = weapons.KNOCKBACK_MAGIC)
        
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
                         owner_pos=owner,
                         knockback = weapons.KNOCKBACK_LUNE)
                
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
                         owner_pos=owner,
                         knockback = weapons.KNOCKBACK_LASER)
        
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
                         owner_pos=owner,
                         weight = weapons.POMPE_WEIGHT,
                         knockback = weapons.KNOCKBACK_POMPE)
        
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
                         owner_pos=owner,
                         knockback = weapons.KNOCKBACK_STONE)
        
class Lance(Projectile) :

    def __init__(self,angle,pos,team,randomize,owner):

        self.life_time = weapons.LANCE_LIFE

        super().__init__(pos,self.life_time,angle,
                         speed = weapons.LANCE_V,
                         id_img = 8,
                         width = weapons.LANCE_WIDTH,
                         height = weapons.LANCE_HEIGHT,
                         damage = weapons.LANCE_DAMAGE,
                         team=team,
                         randomize_angle=randomize,
                         owner_pos=owner,
                         knockback = weapons.KNOCKBACK_LANCE)
        
class Death(Projectile) :

    def __init__(self,angle,pos,team,randomize,owner):

        self.life_time = weapons.DEATH_LIFE

        super().__init__(pos,self.life_time,angle,
                         speed = weapons.DEATH_V,
                         id_img = 9,
                         width = weapons.DEATH_WIDTH,
                         height = weapons.DEATH_HEIGHT,
                         damage = weapons.DEATH_DAMAGE,
                         team=team,
                         randomize_angle=randomize,
                         owner_pos=owner,)
        
class Lanterne(Projectile) :

    def __init__(self,angle,pos,team,randomize,owner):

        self.life_time = weapons.LANTERNE_LIFE

        super().__init__(pos,self.life_time,angle,
                         speed = weapons.LANTERNE_V,
                         id_img = 44,
                         width = weapons.LANTERNE_WIDTH,
                         height = weapons.LANTERNE_HEIGHT,
                         damage = weapons.LANTERNE_DAMAGE,
                         team=team,
                         randomize_angle=randomize,
                         weight = weapons.LANTERNE_WEIGHT,
                         rebond = True,
                         owner_pos=owner,)
        self.can_damage = False
        
class Fluff(Projectile) :

    def __init__(self,angle,pos,team,randomize,owner):

        self.life_time = weapons.LANTERNE_LIFE
        delta_angle = random.randint(-weapons.FLUFF_RANDOM_ANGLE,weapons.FLUFF_RANDOM_ANGLE)

        super().__init__(pos,self.life_time,(angle+delta_angle)%360,
                         id_img = 45,
                         speed = weapons.FLUFF_V,
                         width = weapons.FLUFF_WIDTH,
                         height = weapons.FLUFF_HEIGHT,
                         damage = weapons.FLUFF_DAMAGE,
                         team=team,
                         randomize_angle=randomize,
                         weight = weapons.FLUFF_WEIGHT,
                         rebond = True,
                         owner_pos=owner,)
        
        self.delta_angle = delta_angle%360
        
class Big_Lune(Projectile) :

    def __init__(self,angle,pos,team,randomize,owner):

        self.life_time = weapons.BIG_LUNE_LIFE

        super().__init__(pos,self.life_time,angle,
                         speed = weapons.BIG_LUNE_V,
                         id_img = 48,
                         width = weapons.BIG_LUNE_WIDTH,
                         height = weapons.BIG_LUNE_HEIGHT,
                         damage = weapons.BIG_LUNE_DAMAGE,
                         team=team,
                         randomize_angle=randomize,
                         owner_pos=owner,
                         knockback = weapons.KNOCKBACK_LUNE)