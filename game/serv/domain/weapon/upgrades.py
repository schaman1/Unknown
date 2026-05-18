from serv.domain.projectile import projectile_type
from shared.constants.world import RATIO
from serv.config import weapons
from serv.domain.mob.team import Team


class Upgrade:

    def __init__(self,id,time_take):

        self.id = id
        self.time_take = time_take
        self.ratio = RATIO

def AddProjectileWhenDie(projectile,weapon):
    """If want to update it can make that if put dash after bdf, dash trigger when bdf touch ?"""
    
    next_projectiles,next_id_event_player = weapon.trigger_shot(weapon.angle,weapon.pos)

    projectile.projectile_spawn_when_die=next_projectiles

#class CreateMagic(Upgrade): #Not use
#
#    def __init__(self):
#
#        super().__init__(id = 1,time_take = weapons.MAGIC_RELOAD_TIME)
#
#    def trigger(self,weapon):
#
#        projectile = weapon.add_projectile(projectile_type.Magic(weapon.angle,weapon.pos,weapon.team,weapon.randomize_angle))
#
#        return 1,[projectile],None
#
class CreateFire(Upgrade):

    def __init__(self):

        super().__init__(id = 2,time_take =weapons.FIRE_RELOAD_TIME)

    def trigger(self,weapon):

        projectile = weapon.add_projectile(projectile_type.Fire(weapon.angle,weapon.pos,weapon.team,weapon.randomize_angle))

        return 1,[projectile],None
    
class CreateLune(Upgrade):

    def __init__(self):

        super().__init__(id=3,time_take = weapons.LUNE_RELOAD_TIME)

    def trigger(self,weapon):

        projectile = weapon.add_projectile(projectile_type.Lune(weapon.angle,weapon.pos,weapon.team,weapon.randomize_angle))

        return 1,[projectile],None
    
class CreatePompe(Upgrade):

    def __init__(self):

        super().__init__(id=4,time_take = weapons.POMPE_RELOAD_TIME)

    def trigger(self,weapon):

        projectiles = []

        angle = (weapon.angle - weapons.POMPE_DISPERSION)%360
        proj = projectile_type.Pompe(angle,weapon.pos,weapon.team,weapon.randomize_angle)
        proj.delta_angle = -weapons.POMPE_DISPERSION
        projectiles.append(weapon.add_projectile(proj))
        
        angle+= weapons.POMPE_DISPERSION
        angle = angle%360
        proj = projectile_type.Pompe(angle,weapon.pos,weapon.team,weapon.randomize_angle)
        projectiles.append(weapon.add_projectile(proj))
        
        angle+= weapons.POMPE_DISPERSION
        angle = angle%360
        proj = projectile_type.Pompe(angle,weapon.pos,weapon.team,weapon.randomize_angle)
        proj.delta_angle = weapons.POMPE_DISPERSION
        projectiles.append(weapon.add_projectile(proj))

        return 1,projectiles,None
    
class CreateLaser(Upgrade):

    def __init__(self):

        super().__init__(id=5,time_take = weapons.LASER_RELOAD_TIME)

    def trigger(self,weapon):

        projectile = weapon.add_projectile(projectile_type.Laser(weapon.angle,weapon.pos,weapon.team,weapon.randomize_angle))

        return 1,[projectile],None
    
class AddSpeed(Upgrade):

    def __init__(self):

        super().__init__(id = 10,time_take=0)

    def trigger(self,weapon):

        weapon.speed_mult+=1

        return 0,None,None
    
class AddRebond(Upgrade):
    #Ajoute rebond a tout les prohcains tir mais leur enleve 2 dégat

    def __init__(self):

        super().__init__(id = 11,time_take=0)

    def trigger(self,weapon):

        weapon.add_rebond=True

        weapon.add_damage -=2

        return 0,None,None
    
class Randomizer(Upgrade):
    #Randomize la direction mais reduit le temps de rechargement de l'arme

    def __init__(self):

        super().__init__(id = 12,time_take = weapons.RANDOMIZER_RELOAD_TIME)

        self.minus_refill_time = weapons.RANDOMIZER_REFILL_TIME

    def trigger(self,weapon):

        weapon.randomize_angle = True
        weapon.loading_time_refill_current += self.minus_refill_time

        return 0,None,None
    
class AddDamage(Upgrade):
    #Randomize la direction mais reduit le temps de rechargement de l'arme

    def __init__(self):

        super().__init__(id = 13,time_take = 0)

    def trigger(self,weapon):

        weapon.add_damage +=3
        weapon.team = Team.All

        return 0,None,None
    
class DoubleSpell(Upgrade):

    def __init__(self):

        super().__init__(id = 20,time_take=0)

    def trigger(self,weapon):

        return -1,None,None #Done un slot de plus de disponible
    
class TripleSpell(Upgrade):

    def __init__(self):

        super().__init__(id = 21,time_take=0)

    def trigger(self,weapon):

        return -1,None,None #Done un slot de plus de disponible
    
class CreateFire_DieEffect(Upgrade):
    """DieEffect = create projectile when die"""

    def __init__(self):

        super().__init__(id = 30,time_take = weapons.FIRE_RELOAD_TIME_DIE_EFFECT)

    def trigger(self,weapon):

        projectile = projectile_type.Fire(weapon.angle,weapon.pos,weapon.team,weapon.randomize_angle)

        projectile = weapon.add_projectile(projectile)

        AddProjectileWhenDie(projectile,weapon)

        return 1,[projectile],None
    
class SmallDash(Upgrade):

    def __init__(self):

        super().__init__(id=40,time_take=weapons.SMALL_DASH_RELOAD_TIME)
        self.time_dash_take = 0.1
        self.distance_dash = 5*self.ratio

    def trigger(self,weapon):

        return 1,None,[self.id,[0,self.time_dash_take,self.distance_dash,weapon.angle]]
    
class LongDash(Upgrade):

    def __init__(self):

        super().__init__(id=41,time_take=weapons.LONG_DASH_RELOAD_TIME)
        self.time_dash_take = 0.1
        self.distance_dash = 10*self.ratio

    def trigger(self,weapon):

        return 1,None,[self.id,[0,self.time_dash_take,self.distance_dash,weapon.angle]]
    
class Jump(Upgrade):

    def __init__(self):

        super().__init__(id=42,time_take=weapons.JUMP_RELOAD)

    def trigger(self,weapon):

        return 1,None,[self.id]
    
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

UPGRADES = {}
#UPGRADES[1] = CreateMagic()
UPGRADES[2] = CreateFire()
UPGRADES[3] = CreateLune()
UPGRADES[4] = CreatePompe()
UPGRADES[5] = CreateLaser()
UPGRADES[10] = AddSpeed()
UPGRADES[11] = AddRebond()
UPGRADES[12] = Randomizer()
UPGRADES[13] = AddDamage()
UPGRADES[20] = DoubleSpell()
UPGRADES[21] = TripleSpell()
UPGRADES[30] = CreateFire_DieEffect()
UPGRADES[40] = SmallDash()
UPGRADES[41] = LongDash()
UPGRADES[42] = Jump()