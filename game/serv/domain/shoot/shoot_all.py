from serv.domain.shoot import weapon

class Shoot_all :

    def __init__(self):
        self.next_id = 0
        self.l_Shoot = []

    def generate_id(self):
        self.next_id = (self.next_id+1) % 65536 #Maximum pour uint16
        return self.next_id
    
    def create_shoot(self,type_weapon,angle,pos):
        
        if type_weapon == "pioche" :
            self.l_Shoot.append(weapon.Pioche(self.generate_id(),angle,pos))