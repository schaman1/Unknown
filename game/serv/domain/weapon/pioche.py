from serv.config import weapons
from serv.domain.weapon.base_weapon import Weapon
from serv.domain.projectile.projectile_type import Pioche


class PiocheWeapon(Weapon) :

    def __init__(self):

        super().__init__(
            loading_time = weapons.LOAD_PIOCHE,
            vitesse = weapons.V_PIOCHE,
            life = weapons.LIFE_PIOCHE,
            damage = weapons.DAMAGE_PIOCHE,
            id = weapons.ID_PIOCHE
        )

    def create_projectile(self,id,angle,pos):
        return Pioche(id,angle,pos)
