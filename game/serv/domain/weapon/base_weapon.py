

class Weapon :

    def __init__(self,loading_time,nbr_slot,nbr_upgrades_trigger,id):
        
        self.loading_time = int(loading_time)
        self.id = id

        self.spells_on_shot = [None for _ in range(nbr_slot)]
        self.projectile_shot = []
        self.nbr_upgrades_trigger_max = nbr_upgrades_trigger
        self.nbr_upgrades_trigger = 0
        self.nbr_spells_max = len(self.spells_on_shot)

        self.speed_mult = 1

        self.angle = 0
        self.pos = 0
        self.idx = 0

    def return_info(self,i):
        spells_id = []
        for weapon in self.spells_on_shot :
            if weapon == None :
                spells_id.append(0)
                
            else :
                spells_id.append(weapon.id)

        return i,self.id,self.loading_time,self.nbr_spells_max,spells_id

    def reset_values(self):
        self.projectile_shot.clear()
        self.speed_mult = 1
        self.nbr_upgrades_trigger = 0

        if self.idx == self.nbr_spells_max :
            self.idx = 0


    def create_projectile(self,angle,pos):

        self.reset_values()
        
        self.angle = angle
        self.pos = pos

        while self.nbr_upgrades_trigger < self.nbr_upgrades_trigger_max and self.idx < self.nbr_spells_max :

            spell = self.spells_on_shot[self.idx]

            if spell != None : 

                self.nbr_upgrades_trigger+=spell.trigger(self)

            self.idx+=1

        return self.projectile_shot