from serv.domain.projectile import projectile_type
from shared.constants.world import RATIO

class Upgrade:

    def __init__(self,id,time_take):

        self.id = id
        self.time_take = time_take
        self.ratio = RATIO

def AddProjectileWhenDie(projectile,weapon):
    
    next_projectiles,next_time = weapon.create_projectile(weapon.angle,weapon.pos,weapon.team)

    projectile.projectile_spawn_when_die=next_projectiles

class CreateFire(Upgrade):

    def __init__(self):

        super().__init__(id = 1,time_take =0.1)

    def trigger(self,weapon):

        projectile = weapon.add_projectile(projectile_type.Fire(weapon.angle,weapon.pos,weapon.team))

        return 1,projectile,None
    
class CreateMagic(Upgrade):

    def __init__(self):

        super().__init__(id = 2,time_take = 0.1)

    def trigger(self,weapon):

        projectile = weapon.add_projectile(projectile_type.Magic(weapon.angle,weapon.pos,weapon.team))

        return 1,projectile,None
    
class CreateLune(Upgrade):

    def __init__(self):

        super().__init__(id=3,time_take = 0.1)

    def trigger(self,weapon):

        projectile = weapon.add_projectile(projectile_type.Lune(weapon.angle,weapon.pos,weapon.team))

        return 1,projectile,None
    
class AddSpeed(Upgrade):

    def __init__(self):

        super().__init__(id = 10,time_take=0)

    def trigger(self,weapon):

        weapon.speed_mult+=2

        return 0,None,None
    
class AddRebond(Upgrade):
    #Ajoute rebond a tout les prohcains tir mais leur enleve 2 dégat

    def __init__(self):

        super().__init__(id = 11,time_take=0)

    def trigger(self,weapon):

        weapon.add_rebond=True

        weapon.add_damage = -2

        return 0,None,None
    
class DoubleSpell(Upgrade):

    def __init__(self):

        super().__init__(id = 20,time_take=0.1)

    def trigger(self,weapon):

        return -1,None,None #Done un slot de plus de disponible
    
class CreateFire_DieEffect(Upgrade):
    """DieEffect = create projectile when die"""

    def __init__(self):

        super().__init__(id = 30,time_take =0.1)

    def trigger(self,weapon):

        projectile = projectile_type.Fire(weapon.angle,weapon.pos)

        projectile = weapon.add_projectile(projectile)

        AddProjectileWhenDie(projectile,weapon)

        return 1,projectile,None
    
class SmallDash(Upgrade):

    def __init__(self):

        super().__init__(id=3,time_take=0.0)
        self.time_dash_take = 0.05
        self.distance_dash = 8*self.ratio

    def trigger(self,weapon):

        return 1,None,[self.id,[0,self.time_dash_take,self.distance_dash,weapon.angle]]

    
#Remove too difficult and useless
#class AddSize(Upgrade):
#    def __init__(self):
#
#        super().__init__(id = 5,time_take=0)
#
#    def trigger(self,weapon):
#
#        weapon.size_mult +=2
#
#        return 0
