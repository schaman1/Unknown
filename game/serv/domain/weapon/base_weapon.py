import time

class Weapon :

    def __init__(self,refill_time,spell_time,nbr_slot,nbr_upgrades_trigger,id):
        
        self.loading_time_refill = refill_time
        self.loading_time_spell = spell_time
        self.id = id

        self.spells_on_shot = [None for _ in range(nbr_slot)]
        self.projectile_shot = []
        self.nbr_upgrades_trigger_max = nbr_upgrades_trigger
        self.nbr_upgrades_trigger = 0
        self.nbr_spells_max = len(self.spells_on_shot)
        self.next_allowed_shot = 0

        self.speed_mult = 1
        self.add_rebond = False
        self.add_damage = 0

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

        return i,self.id,self.nbr_spells_max,spells_id

    def reset_values(self):
        self.projectile_shot.clear()
        self.speed_mult = 1
        self.add_rebond = False
        self.nbr_upgrades_trigger = 0

        if self.idx == self.nbr_spells_max :
            self.idx = 0

    def check_can_shot(self,now):
        
        if now >= self.next_allowed_shot :
            return True
        
        else :
            return False
        
    def add_projectile(self,projectile_type):
        projectile = projectile_type(self.angle,self.pos,self.speed_mult)

        if self.add_rebond :
            projectile.rebond = True

        projectile.damage += self.add_damage
            
        self.projectile_shot.append(projectile)

    def create_projectile(self,angle,pos):

        now = time.perf_counter()

        if not self.check_can_shot(now):  #Pour enlever la contraite de tir niveau serveur
            return 

        self.reset_values()
        
        self.angle = angle
        self.pos = pos

        self.time_spells_take = 0

        while self.nbr_upgrades_trigger < self.nbr_upgrades_trigger_max and self.idx < self.nbr_spells_max :

            spell = self.spells_on_shot[self.idx]

            if spell != None : 

                self.nbr_upgrades_trigger+=spell.trigger(self)

                self.time_spells_take+=spell.time_take

            self.idx+=1

        self.time_spells_take+=self.loading_time_spell

        if self.idx==self.nbr_spells_max :
            self.next_allowed_shot = now+max(self.time_spells_take,self.loading_time_refill)
        else :
            self.next_allowed_shot = now+self.time_spells_take

        return self.projectile_shot,int((self.next_allowed_shot-now)*1000)