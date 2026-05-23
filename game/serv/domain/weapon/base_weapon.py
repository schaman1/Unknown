import time,math

class Weapon :

    def __init__(self,refill_time,spell_time,nbr_slot,nbr_upgrades_trigger,id,team,player):
        
        self.loading_time_refill = refill_time
        self.loading_time_refill_current = refill_time
        self.loading_time_spell = spell_time
        self.loading_time_spell_current = spell_time
        self.min_delay = 0.015#Delay minimum de recgarge, peut pas faire moins !


        self.team=team
        self.reel_team = self.team
        self.id = id
        self.owner = player

        self.spells_on_shot = [None for _ in range(nbr_slot)]
        self.nbr_slot = nbr_slot
        self.nbr_upgrades_trigger_max = nbr_upgrades_trigger
        self.nbr_spells_max = len(self.spells_on_shot)
        self.next_allowed_shot = 0

        self.size_mult = 1
        self.speed_mult = 1
        self.add_life = 0
        self.add_rebond = False
        self.add_damage = 0
        self.randomize_angle = False

        self.angle = 0
        self.pos = 0
        self.idx = 0

    def return_info(self,i):
        spells_id = []
        for upgrade in self.spells_on_shot :
            if upgrade == None :
                spells_id.append(0)
                
            else :
                spells_id.append(upgrade.id)

        return i,self.id,self.nbr_spells_max,spells_id
    
    def del_spell(self,id_spell):
        id = self.spells_on_shot[id_spell].id
        self.spells_on_shot[id_spell]=None

        return id

    def reset_values(self):
        self.team = self.reel_team
        self.speed_mult = 1
        self.size_mult = 1
        self.add_damage = 0
        self.add_life = 0
        self.add_rebond = False
        self.randomize_angle = False
        self.next_allowed_shot_time = 0
        self.loading_time_refill_current = self.loading_time_refill
        self.loading_time_spell_current = self.loading_time_spell

        if self.idx == self.nbr_spells_max :
            self.idx = 0

    def return_info_next_time_can_shot(self):
        
        return int(self.next_allowed_shot_time*1000)

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

        projectile.damage = max(1,self.add_damage+projectile.damage) #Min 1 degat
        projectile.speed = projectile.speed*self.speed_mult
        projectile.life_time += self.add_life

        projectile.width=int(projectile.width*self.size_mult)
        projectile.height=int(projectile.height*self.size_mult)

        projectile.owner = self.owner

    def trigger_shot(self,angle,pos):

        now = time.perf_counter()

        if not self.check_can_shot(now):  #Pour enlever la contraite de tir niveau serveur
            return 

        self.reset_values()
        infos,cast_min_1_spell = self.create_projectile(angle,pos,self.nbr_upgrades_trigger_max,idx = self.idx)

        self.update_reload_time_wand(now,cast_min_1_spell)

        return infos

    def update_reload_time_wand(self,now,has_cast_1_spell):

        if not has_cast_1_spell :
            self.next_allowed_shot = now
            self.next_allowed_shot_time = 0
            return
        
        if self.test_if_last_spell_of_weapon() :
            self.idx = 0
            self.next_allowed_shot = max(self.next_allowed_shot,now+max(self.loading_time_spell_current,self.loading_time_refill_current))
            
        else :
            self.next_allowed_shot = max(self.next_allowed_shot,now+self.loading_time_spell_current)

        self.next_allowed_shot = max(self.next_allowed_shot,now+self.min_delay)
        self.next_allowed_shot_time = self.next_allowed_shot - now

        #if self.team ==0:
        #    print(self.next_allowed_shot-now,"Time loading :",self.loading_time_spell_current,self.loading_time_spell)
        #    print("TIme refill :",self.loading_time_refill_current,self.loading_time_refill)
        #    print("Send client : ",self.next_allowed_shot_time)

    def create_projectile(self,angle,pos,nbr_trigger = 1,idx = 0):

        projectile_shot = []
        event_player = []

        has_cast_1_spell = False
        
        self.angle = angle
        self.pos = pos

        while nbr_trigger>0 and self.idx < self.nbr_spells_max :

            spell = self.spells_on_shot[self.idx]

            self.idx+=1
            #idx+=1

            if spell != None : 

                has_cast_1_spell = True

                space_take,projectiles,id_event_player = spell.trigger(self,self.idx-1)

                nbr_trigger-= space_take

                if projectiles!=None and projectiles != [] :
                    
                    for i in range(len(projectiles)):
                        projectile_shot.append(projectiles[i])

                if id_event_player!=None:
                    event_player.append(id_event_player)

                self.loading_time_spell_current+=spell.time_take


        self.update_pos_projectile(angle,projectile_shot)

        return [projectile_shot,event_player],has_cast_1_spell
    
    def update_pos_projectile(self,angle,projectiles):
        """All projectiles are created in front of the player BUT ! We need to had the size of the projectile to the pos !"""

        vx = math.cos(math.radians(angle))
        vy = math.sin(math.radians(angle))

        for projectile in projectiles :

            projectile.pos_x += vx*(projectile.half_width+100)
            projectile.pos_y -= vy*(projectile.half_width+100)
    
    def test_if_last_spell_of_weapon(self):
        
        i = self.idx

        while i<self.nbr_spells_max and self.spells_on_shot[i] == None:
            i+=1

        return i>=self.nbr_spells_max

    def fill_slot(self,idx,function):

        if idx >= len(self.spells_on_shot):
            print("Unable to fill spot in weapon bcs idx tooo high")

        else :
            self.spells_on_shot[idx]=function

    def add_slot(self,i):
        self.nbr_slot+=1
        self.spells_on_shot.append(None)
        self.nbr_spells_max+=1

        return self.return_info(i)