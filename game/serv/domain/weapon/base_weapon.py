import time

class Weapon :

    def __init__(self,refill_time,spell_time,nbr_slot,nbr_upgrades_trigger,id):
        
        self.loading_time_refill = refill_time
        self.loading_time_spell = spell_time
        self.id = id

        self.spells_on_shot = [None for _ in range(nbr_slot)]
        self.nbr_upgrades_trigger_max = nbr_upgrades_trigger
        self.nbr_upgrades_trigger = 0
        self.nbr_spells_max = len(self.spells_on_shot)
        self.next_allowed_shot = 0

        self.size_mult = 1
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

        #print("spells_id",self.nbr_spells_max)

        return i,self.id,self.nbr_spells_max,spells_id

    def reset_values(self):
        self.speed_mult = 1
        self.size_mult = 1
        self.add_rebond = False
        self.nbr_upgrades_trigger = 0

        if self.idx == self.nbr_spells_max :
            self.idx = 0

    def return_info_next_time_can_shot(self):
        #print(self.next_allowed_shot,time.perf_counter())
        
        return int((self.next_allowed_shot-time.perf_counter())*1000)

    def check_can_shot(self,now):
        
        if now >= self.next_allowed_shot :
            return True
        
        else :
            return False
        
    def add_projectile(self,projectile):

        self.add_upgrades_to_projectile(projectile)

        projectile.load()
            
        return projectile

    def add_upgrades_to_projectile(self,projectile):

        if self.add_rebond :
            projectile.rebond = True

        projectile.damage += self.add_damage
        projectile.speed = projectile.speed*self.speed_mult

        projectile.width=int(projectile.width*self.size_mult)
        projectile.height=int(projectile.height*self.size_mult)

    def trigger_shot(self,angle,pos):

        now = time.perf_counter()

        if not self.check_can_shot(now):  #Pour enlever la contraite de tir niveau serveur
            return 

        self.reset_values()

        return self.create_projectile(angle,pos,now)

    def create_projectile(self,angle,pos,now=time.perf_counter()):

        projectile_shot = []
        event_player = []
        
        self.angle = angle
        self.pos = pos

        self.time_spells_take = 0

        while self.nbr_upgrades_trigger < self.nbr_upgrades_trigger_max and self.idx < self.nbr_spells_max :

            spell = self.spells_on_shot[self.idx]
            self.idx+=1

            if spell != None : 

                space_take,projectile,id_event_player = spell.trigger(self)

                self.nbr_upgrades_trigger+= space_take

                if projectile!=None :
                    projectile_shot.append(projectile)

                if id_event_player!=None:
                    event_player.append(id_event_player)

                self.time_spells_take+=spell.time_take

        self.time_spells_take+=self.loading_time_spell

        if self.idx==self.nbr_spells_max :
            self.next_allowed_shot = now+max(self.time_spells_take,self.loading_time_refill)
        else :
            self.next_allowed_shot = now+self.time_spells_take

        #print(projectile,event_player)

        return [projectile_shot,event_player]