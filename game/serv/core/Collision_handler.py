from serv.domain.mob.team import Team

class CollisionHandler:

    def __init__(self):
        self.effect_send = []
        self.die_send = []

        self.ent_touch = {}

    def trigger_collision(self,mobs,friendly_mobs,players,projectiles):

        for chunk,l_projectile in projectiles.items() : 

            for projectile in l_projectile:

                if projectile.team!=Team.Player:

                    if projectile.movable == False :
                        chunks = self.return_chunk_neigborns(chunk,mobs)

                    else :
                        chunks = [chunk]

                    for in_chunk in chunks :

                        for mob in friendly_mobs[in_chunk] :

                            touch = self.collision(projectile,mob)

                            if touch :
                                self.handle_touch(projectile,mob,in_chunk)

                    for player in players.values() :

                        if not player.is_dead :

                            touch = self.collision(projectile,player)

                            if touch :

                                self.player_take_damage(projectile,player)
                        
                if projectile.team!=Team.Mob:

                    if projectile.movable == False :
                        chunks = self.return_chunk_neigborns(chunk,mobs)

                    else :
                        chunks = [chunk]

                    for in_chunk in chunks :

                        for mob in mobs[in_chunk] :

                            touch = self.collision(projectile,mob)

                            if touch :
                                self.handle_touch(projectile,mob,in_chunk)

        self.trigger_ent_touch()

    def return_chunk_neigborns(self,chunk,mobs):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-100, 0, 100]:
                neighbor = chunk + dx + dy
                if neighbor in mobs:
                    neighbors.append(neighbor)
        return neighbors

    def collision(self,ent1,ent2):

        pos1 = (ent1.pos_x,ent1.pos_y)
        pos2 = (ent2.pos_x,ent2.pos_y)

        #print("projectile : ",pos1,ent1.width,ent1.height)
        #print("mob : ",pos2,ent2.width,ent2.height)

        bool_res = self.collision_rec(pos1,ent1.width,ent1.height,pos2,ent2.width,ent2.height)

        return bool_res
    
    def collision_rec(self, center1, width1, height1, center2, width2, height2):

        xleft1,  xright1 = center1[0] - width1  / 2, center1[0] + width1  / 2
        yleft1,  yright1 = center1[1] - height1 / 2, center1[1] + height1 / 2

        xleft2,  xright2 = center2[0] - width2  / 2, center2[0] + width2  / 2
        yleft2,  yright2 = center2[1] - height2 / 2, center2[1] + height2 / 2

        overlap_x = xleft1 <= xright2 and xright1 >= xleft2
        overlap_y = yleft1 <= yright2 and yright1 >= yleft2

        return overlap_x and overlap_y
    
    def player_take_damage(self,projectile,player,chunk=99):

        old_pv = player.life
        die = player.take_damage(projectile.damage)
        delta_life = old_pv-player.life

        if delta_life<0:
            print("Issue with delta life negatif in : serv/core/collision_handler",delta_life)
        
        else :

            if delta_life != 0:
                self.effect_send.append([player.id,delta_life,chunk])

            if die:
                print("PLayer is dead")
                self.die_send.append([player.id,chunk,player.len_dead])

            projectile.is_dead = True

    def player_take_damage_no_projectile(self,damage,player,chunk=99):

        if player.dead :
            return

        old_pv = player.life
        die = player.take_damage(damage)
        delta_life = old_pv-player.life

        if delta_life<0:
            print("Issue with delta life negatif in : serv/core/collision_handler",delta_life)
        
        else :

            if delta_life != 0:

                self.effect_send.append([player.id,delta_life,chunk])

                if die :
                    if player.auto_destruction :
                        player.time_destroy = 0 #Means destroy
                    else :
                        self.die_send.append([player.id,chunk,player.len_dead])

    
    def add_ent_touch(self,ent,projectile,chunk):

        knockback = getattr(projectile,'knockback',0)

        if ent.id in self.ent_touch :
            self.ent_touch[ent.id][0]+=projectile.damage
            #Keep the strongest knockback among projectiles hitting this ent this frame
            self.ent_touch[ent.id][4] = max(self.ent_touch[ent.id][4],knockback)

        else :
            self.ent_touch[ent.id] = [projectile.damage,projectile.owner,chunk,ent,knockback]

    def handle_touch(self,projectile,ent,chunk):

        self.add_ent_touch(ent,projectile,chunk)

        projectile.is_dead = True

    def trigger_ent_touch(self):

        for ent_id,(damage,owner,chunk,ent,knockback) in self.ent_touch.items():

            old_pv = ent.life

            die = ent.take_damage(damage,owner,knockback)

            delta_life = old_pv-ent.life

            if not ent.dead or delta_life != 0:

                self.effect_send.append([ent.id,delta_life,chunk])
             
            if die:
                if ent.auto_destruction :
                    ent.time_destroy = 0 #Means destroy
                else :
                    self.die_send.append([ent.id,chunk,ent.len_dead])

        self.ent_touch.clear()

    def check_if_touch_damage_obj(self,map,dt,player):
        """Take damage. If stay 0.5 sec, die"""

        if player.touch_element(map,map.kill):

            damage = int(250*dt)

            self.player_take_damage_no_projectile(damage,player,chunk=99)
