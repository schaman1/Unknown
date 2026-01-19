from serv.domain.projectile import projectile_type

class Upgrade:

    def __init__(self,id,time_take):

        self.id = id
        self.time_take = time_take

class CreateFireball(Upgrade):

    def __init__(self):

        super().__init__(id = 1,time_take =0.1)

    def trigger(self,weapon):

        weapon.add_projectile(projectile_type.Fireball)

        return 1
    
class AddSpeed(Upgrade):

    def __init__(self):

        super().__init__(id = 2,time_take=0)

    def trigger(self,weapon):

        weapon.speed_mult+=2

        return 0
    
    
class DoubleSpell(Upgrade):

    def __init__(self):

        super().__init__(id = 3,time_take=0.1)

    def trigger(self,weapon):

        return -1 #Done un slot de plus de disponible
    
class AddRebond(Upgrade):
    #Ajoute rebond a tout les prohcains tir mais leur enleve 2 dégat

    def __init__(self):

        super().__init__(id = 4,time_take=0)

    def trigger(self,weapon):

        weapon.add_rebond=True

        weapon.add_damage = -2

        return 0