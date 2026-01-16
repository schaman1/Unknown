

class Weapon :

    def __init__(self,loading_time,nbr_slot,nbr_upgrades_trigger,id):
        
        self.loading_time = loading_time

        self.id = id

        self.spells_on_shot = [None for _ in range(nbr_slot)]
        self.projectile_shot = []
        self.speed_mult = 1

        self.angle = 0
        self.pos = 0

    def reset_values(self):
        self.projectile_shot.clear()
        self.speed_mult = 1


    def create_projectile(self,angle,pos):

        self.reset_values()
        
        self.angle = angle
        self.pos = pos


        for spell in self.spells_on_shot :

            if spell != None : 

                spell(self)

        return self.projectile_shot