from serv.domain.shoot.default_shoot import Shoot
from serv.config import weapons

class Pioche(Shoot) :

    def __init__(self,id,angle,pos):

        self.vitesse = weapons.V_PIOCHE
        self.life_time = weapons.LIFE_PIOCHE


        super.__init__(pos,self.life_time,id,angle,self.vitesse)



