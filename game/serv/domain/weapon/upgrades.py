from serv.domain.projectile import projectile_type

def create_fireball(weapon):

    weapon.projectile_shot.append(projectile_type.Fireball(weapon.angle,weapon.pos,weapon.speed_mult))

def add_speed(weapon):

    weapon.speed_mult+=2