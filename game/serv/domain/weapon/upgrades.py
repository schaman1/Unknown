from serv.domain.projectile import projectile_type

class Upgrade:

    def __init__(self,id):

        self.id = id

class CreateFireball(Upgrade):

    def __init__(self):

        super().__init__(id = 1)

    def trigger(self,weapon):

        weapon.projectile_shot.append(projectile_type.Fireball(weapon.angle,weapon.pos,weapon.speed_mult))

        return 1
    
class AddSpeed(Upgrade):

    def __init__(self):

        super().__init__(id = 2)

    def trigger(self,weapon):

        weapon.speed_mult+=2

        return 0
    
class DoubleSpell(Upgrade):

    def __init__(self):

        super().__init__(id = 3)

    def trigger(self,weapon):

        return -1 #Done un slot de plus de disponible