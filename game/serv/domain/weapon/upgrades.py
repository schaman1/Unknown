from serv.domain.projectile import projectile_type
from shared.constants.world import RATIO
from serv.config import weapons
from serv.domain.mob.team import Team


class Upgrade:

    def __init__(self,id,time_take):

        self.id = id
        self.time_take = time_take
        self.ratio = RATIO

def AddProjectileWhenDie(projectiles,weapon,idx = 0):
    """If want to update it can make that if put dash after bdf, dash trigger when bdf touch ?"""

    if not weapon.test_if_last_spell_of_weapon() :
    
        infos,_ = weapon.create_projectile(weapon.angle,weapon.pos,idx = weapon.idx)
        next_projectiles,_ = infos

    else :
        next_projectiles = []

    #for projectile in projectiles :
    for i in range(len(projectiles)):

        if i == 0: #Don't copy the first One
            for proj in next_projectiles :
                projectiles[i].projectile_spawn_when_die.append(proj)

        else :
            l = copy_projectiles(next_projectiles)
            for proj in l:
                projectiles[i].projectile_spawn_when_die.append(proj)
    
def copy_projectiles(source):
        copy = []
        for proj in source :
            proj_copy = proj.__class__(proj.angle,[proj.pos_x,proj.pos_y],proj.team,proj.randomize_angle,proj.owner_pos)
            
            proj_copy.force_angle = proj.force_angle
            proj_copy.force_pos = proj.force_pos
            proj_copy.delta_angle = proj.delta_angle
            proj_copy.delta_pos = [proj.delta_pos[0],proj.delta_pos[1]]
            proj_copy.angle_force = proj.angle_force
            proj_copy.owner = proj.owner

            proj_copy.life_time = proj.life_time
            proj_copy.damage = proj.damage
            proj_copy.speed = proj.speed
            proj_copy.rebond = proj.rebond

            
            copy.append(proj_copy)

            proj_when_die = copy_projectiles(proj.projectile_spawn_when_die)
            proj_copy.projectile_spawn_when_die = proj_when_die

        return copy

class CreateFire(Upgrade):

    def __init__(self):

        super().__init__(id = 2,time_take =weapons.FIRE_RELOAD_TIME)

    def trigger(self,weapon,idx=0):

        projectile = weapon.add_projectile(projectile_type.Fire(weapon.angle,weapon.pos,weapon.team,weapon.randomize_angle,weapon.owner.return_pos()))

        return 1,[projectile],None
    
class CreateLune(Upgrade):

    def __init__(self):

        super().__init__(id=3,time_take = weapons.LUNE_RELOAD_TIME)

    def trigger(self,weapon,idx=0):

        projectile = weapon.add_projectile(projectile_type.Lune(weapon.angle,weapon.pos,weapon.team,weapon.randomize_angle,weapon.owner.return_pos()))

        return 1,[projectile],None
    
class CreatePompe(Upgrade):

    def __init__(self):

        super().__init__(id=4,time_take = weapons.POMPE_RELOAD_TIME)

    def trigger(self,weapon,idx=0):

        projectiles = []

        angle = (weapon.angle - weapons.POMPE_DISPERSION)%360
        proj = projectile_type.Pompe(angle,weapon.pos,weapon.team,weapon.randomize_angle,weapon.owner.return_pos())
        proj.delta_angle = -weapons.POMPE_DISPERSION
        projectiles.append(weapon.add_projectile(proj))
        
        angle+= weapons.POMPE_DISPERSION
        angle = angle%360
        proj = projectile_type.Pompe(angle,weapon.pos,weapon.team,weapon.randomize_angle,weapon.owner.return_pos())
        projectiles.append(weapon.add_projectile(proj))
        
        angle+= weapons.POMPE_DISPERSION
        angle = angle%360
        proj = projectile_type.Pompe(angle,weapon.pos,weapon.team,weapon.randomize_angle,weapon.owner.return_pos())
        proj.delta_angle = weapons.POMPE_DISPERSION
        projectiles.append(weapon.add_projectile(proj))

        return 1,projectiles,None
    
class CreateLaser(Upgrade):

    def __init__(self):

        super().__init__(id=5,time_take = weapons.LASER_RELOAD_TIME)

        self.minus_refill_time = weapons.LASER_REFILL_TIME

    def trigger(self,weapon,idx=0):

        weapon.loading_time_refill_current += self.minus_refill_time

        projectile = weapon.add_projectile(projectile_type.Laser(weapon.angle,weapon.pos,weapon.team,weapon.randomize_angle,weapon.owner.return_pos()))

        return 1,[projectile],None
    
class CreateManyLune(Upgrade):

    def __init__(self):

        super().__init__(id=6,time_take = weapons.MANY_LUNE_RELOAD_TIME)

        self.ajout_angle = weapons.MANY_LUNE_DISPERSION

    def trigger(self,weapon,idx=0):

        l = []

        delta_angle = [0,180,270,90]

        delta_pos = weapon.owner.distance_cast_spells*2

        delta_pos_force = []
        dif_pos = []
        for i in range(4):
            delta_pos_force.append([0,0])
            dif_pos.append(weapon.owner.return_pos())

        dif_pos[0][0] += delta_pos
        dif_pos[1][0] -= delta_pos
        dif_pos[2][1] += delta_pos
        dif_pos[3][1] -= delta_pos

        delta_pos_force[0][0] += delta_pos
        delta_pos_force[1][0] -= delta_pos
        delta_pos_force[2][1] += delta_pos
        delta_pos_force[3][1] -= delta_pos

        for i in range(4):
            projectile = weapon.add_projectile(projectile_type.Lune(delta_angle[i],dif_pos[i],weapon.team,weapon.randomize_angle,weapon.owner.return_pos()))
            projectile.damage = weapons.MANY_LUNE_DAMAGE
            projectile.force_angle = True
            projectile.force_pos = True
            projectile.angle_force = projectile.angle
            projectile.delta_pos = [delta_pos_force[i][0],delta_pos_force[i][1]]
            l.append(projectile)

        return 1,l,None

class CreateStone(Upgrade):

    def __init__(self):

        super().__init__(id=7,time_take = weapons.STONE_RELOAD_TIME)

    def trigger(self,weapon,idx=0):
        # projectile = weapon.add_projectile(projectile_type.Stone(weapon.angle,weapon.pos,weapon.team,weapon.randomize_angle,weapon.owner.return_pos()))
        projectile = []
        angle = weapon.angle

        if angle >= 0 and angle <= 50 :
            angle += 35
        elif angle > 155 and angle <= 180 :
            angle -= 35

        elif angle > 100 and angle <= 155 :
            angle -= 20
        elif angle > 50 and angle <= 75 :
            angle += 10

        proj = projectile_type.Stone(angle, weapon.pos, weapon.team, weapon.randomize_angle, weapon.owner.return_pos())
        proj.delta_angle = 0
        projectile.append(weapon.add_projectile(proj))

        angle +=10
        proj = projectile_type.Stone(angle, weapon.pos, weapon.team, weapon.randomize_angle, weapon.owner.return_pos())
        proj.delta_angle =10
        projectile.append(weapon.add_projectile(proj))

        return 1,projectile,None
    
class CreateLance(Upgrade):

    def __init__(self):

        super().__init__(id=8,time_take = weapons.LANCE_RELOAD_TIME)

    def trigger(self,weapon,idx=0):

        projectile = weapon.add_projectile(projectile_type.Lance(weapon.angle,weapon.pos,weapon.team,weapon.randomize_angle,weapon.owner.return_pos()))

        return 1,[projectile],None
    
class CreateDeath(Upgrade):

    def __init__(self):

        super().__init__(id=9,time_take = weapons.DEATH_RELOAD_TIME)

    def trigger(self,weapon,idx=0):

        projectile = weapon.add_projectile(projectile_type.Death(weapon.angle,weapon.pos,weapon.team,weapon.randomize_angle,weapon.owner.return_pos()))

        return 1,[projectile],None
    
class AddSpeed(Upgrade):

    def __init__(self):

        super().__init__(id = 10,time_take=0)

    def trigger(self,weapon,idx=0):

        weapon.speed_mult+=1

        return 0,None,None
    
class AddRebond(Upgrade):
    #Ajoute rebond a tout les prohcains tir mais leur enleve 2 dégat

    def __init__(self):

        super().__init__(id = 11,time_take=0)

    def trigger(self,weapon,idx=0):

        weapon.add_rebond=True

        weapon.add_damage -=2

        return 0,None,None
    
class Randomizer(Upgrade):
    #Randomize la direction mais reduit le temps de rechargement de l'arme

    def __init__(self):

        super().__init__(id = 12,time_take = weapons.RANDOMIZER_RELOAD_TIME)

        self.minus_refill_time = weapons.RANDOMIZER_REFILL_TIME

    def trigger(self,weapon,idx=0):

        weapon.randomize_angle = True
        weapon.loading_time_refill_current += self.minus_refill_time

        return 0,None,None
    
class AddDamage(Upgrade):
    #Randomize la direction mais reduit le temps de rechargement de l'arme

    def __init__(self):

        super().__init__(id = 13,time_take = 0)

    def trigger(self,weapon,idx=0):

        weapon.add_damage +=2
        #weapon.team = Team.All

        return 0,None,None
    
class AddManyDamage(Upgrade):
    #Randomize la direction mais reduit le temps de rechargement de l'arme

    def __init__(self):

        super().__init__(id = 14,time_take = 0)

    def trigger(self,weapon,idx=0):

        weapon.add_damage +=5
        weapon.team = Team.All

        return 0,None,None
    
class Reloader(Upgrade):
    #Randomize la direction mais reduit le temps de rechargement de l'arme

    def __init__(self):

        super().__init__(id = 15,time_take = weapons.RELOADER_RELOAD_TIME)

        self.minus_refill_time = weapons.RELOADER_REFILL_TIME

    def trigger(self,weapon,idx=0):

        #weapon.randomize_angle = True
        weapon.loading_time_refill_current += self.minus_refill_time

        return 0,None,None
    
class AddLife(Upgrade):
    #Randomize la direction mais reduit le temps de rechargement de l'arme

    def __init__(self):

        super().__init__(id = 16,time_take = 0)

        #self.add_life = weapons.ADD_LIFE_AMOUNT

    def trigger(self,weapon,idx=0):

        #weapon.randomize_angle = True
        weapon.add_life += weapons.ADD_LIFE_AMOUNT

        return 0,None,None
    
class DoubleSpell(Upgrade):

    def __init__(self):

        super().__init__(id = 20,time_take=0)

    def trigger(self,weapon,idx=0):

        return -1,None,None #Done un slot de plus de disponible
    
class TripleSpell(Upgrade):

    def __init__(self):

        super().__init__(id = 21,time_take=0)

    def trigger(self,weapon,idx=0):

        return -1,None,None #Done un slot de plus de disponible
    
class AllSpell(Upgrade):

    def __init__(self):

        super().__init__(id = 22,time_take=0)

    def trigger(self,weapon,idx=0):

        return -weapon.nbr_spells_max,None,None #Done un slot de plus de disponible
    
class CreateFire_DieEffect(Upgrade):
    """DieEffect = create projectile when die"""

    def __init__(self):

        super().__init__(id = 30,time_take = weapons.FIRE_RELOAD_TIME_DIE_EFFECT)

    def trigger(self,weapon,idx=0):

        projectile = projectile_type.Fire(weapon.angle,weapon.pos,weapon.team,weapon.randomize_angle,weapon.owner.return_pos())

        projectile = weapon.add_projectile(projectile)

        AddProjectileWhenDie([projectile],weapon,idx)

        return 1,[projectile],None
    
class Copy(Upgrade):
    """DieEffect = create projectile when die"""

    def __init__(self):

        super().__init__(id = 31,time_take = weapons.COPY_RELOAD_TIME)

    def trigger(self,weapon,idx=0):

        idx = idx +1

        while idx < weapon.nbr_spells_max and weapon.spells_on_shot[idx] == None:
            idx +=1

        if idx < weapon.nbr_spells_max :
            spell = weapon.spells_on_shot[idx]
            self.time_take = spell.time_take
            #weapon.idx +=1
            return spell.trigger(weapon,idx = idx)
        
        else : #Don't trigger

            return 0,None,None
    
class CreatePompe_DieEffect(Upgrade):
    """DieEffect = create projectile when die"""

    def __init__(self):

        super().__init__(id = 32,time_take = weapons.POMPE_RELOAD_TIME_DIE_EFFECT)

    def trigger(self,weapon,idx=0):

        projectiles = []

        angle = (weapon.angle - weapons.POMPE_DISPERSION)%360
        proj = projectile_type.Pompe(angle,weapon.pos,weapon.team,weapon.randomize_angle,weapon.owner.return_pos())
        proj.delta_angle = -weapons.POMPE_DISPERSION
        projectiles.append(weapon.add_projectile(proj))
        
        angle+= weapons.POMPE_DISPERSION
        angle = angle%360
        proj = projectile_type.Pompe(angle,weapon.pos,weapon.team,weapon.randomize_angle,weapon.owner.return_pos())
        projectiles.append(weapon.add_projectile(proj))
        
        angle+= weapons.POMPE_DISPERSION
        angle = angle%360
        proj = projectile_type.Pompe(angle,weapon.pos,weapon.team,weapon.randomize_angle,weapon.owner.return_pos())
        proj.delta_angle = weapons.POMPE_DISPERSION
        projectiles.append(weapon.add_projectile(proj))

        AddProjectileWhenDie(projectiles,weapon,idx)

        return 1,projectiles,None
    
class CreateLune_DieEffect(Upgrade):
    """DieEffect = create projectile when die"""

    def __init__(self):

        super().__init__(id = 33,time_take = weapons.LUNE_RELOAD_TIME_DIE_EFFECT)

    def trigger(self,weapon,idx=0):

        projectile = projectile_type.Lune(weapon.angle,weapon.pos,weapon.team,weapon.randomize_angle,weapon.owner.return_pos())

        projectile = weapon.add_projectile(projectile)

        AddProjectileWhenDie([projectile],weapon,idx)
        AddProjectileWhenDie([projectile],weapon,idx)

        return 1,[projectile],None
    
#class SmallDash(Upgrade):
#
#    def __init__(self):
#
#        super().__init__(id=40,time_take=weapons.SMALL_DASH_RELOAD_TIME)
#        self.time_dash_take = 0.1
#        self.distance_dash = 5*self.ratio
#
#    def trigger(self,weapon,idx=0):
#
#        return 1,None,[self.id,[0,self.time_dash_take,self.distance_dash,weapon.angle]]
#    
class LongDash(Upgrade):

    def __init__(self):

        super().__init__(id=41,time_take=weapons.LONG_DASH_RELOAD_TIME)
        self.time_dash_take = 0.1
        self.distance_dash = 10*self.ratio

    def trigger(self,weapon,idx=0):

        return 1,None,[self.id,[0,self.time_dash_take,self.distance_dash,weapon.angle]]
    
#class Jump(Upgrade):
#
#    def __init__(self):
#
#        super().__init__(id=42,time_take=weapons.JUMP_RELOAD)
#
#    def trigger(self,weapon,idx=0):
#
#        return 1,None,[self.id]
    
#Remove too difficult and useless
#class AddSize(Upgrade):
#    def __init__(self):
#
#        super().__init__(id = 5,time_take=0)
#
#    def trigger(self,weapon,idx=0):
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
UPGRADES[6] = CreateManyLune()
UPGRADES[7] = CreateStone()
UPGRADES[8] = CreateLance()
UPGRADES[9] = CreateDeath()
UPGRADES[10] = AddSpeed()
UPGRADES[11] = AddRebond()
UPGRADES[12] = Randomizer()
UPGRADES[13] = AddDamage()
UPGRADES[14] = AddManyDamage()
UPGRADES[15] = Reloader()
UPGRADES[16] = AddLife()
UPGRADES[20] = DoubleSpell()
UPGRADES[21] = TripleSpell()
UPGRADES[22] = AllSpell()
UPGRADES[30] = CreateFire_DieEffect()
UPGRADES[31] = Copy()
UPGRADES[32] = CreatePompe_DieEffect()
UPGRADES[33] = CreateLune_DieEffect()
#UPGRADES[40] = SmallDash()
UPGRADES[41] = LongDash()
#UPGRADES[42] = Jump()

common_upgrades = [2,3,7,8,10,11,12,13,20]
rare_upgrades = [4,5,6,14,21,33,41]
legendary_upgrades = [9,15,22,31,32]