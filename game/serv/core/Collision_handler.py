from serv.domain.mob.team import Team

class CollisionHandler:

    def __init__(self):
        self.effect_send = []
        self.die_send = []

        self.ent_touch = {}

    def trigger_collision(self,mobs,players,projectiles):

        for chunk,l_projectile in projectiles.items() : 

            for projectile in l_projectile:

                if projectile.team!=Team.Player:

                    for player in players.values() :

                        touch = self.collision(projectile,player)

                        if touch :
                            #print("Player touch")
                            self.player_take_damage(projectile,player)
                        
                if projectile.team!=Team.Mob:

                    for mob in mobs[chunk] :


                        touch = self.collision(projectile,mob)

                        if touch :
                            #print("Mob touch")
                            #self.add_ent_touch(mob,projectile.damage)
                            self.handle_touch(projectile,mob,chunk)

        self.trigger_ent_touch()

    def collision(self,ent1,ent2):

        pos1 = (ent1.pos_x,ent1.pos_y)
        pos2 = (ent2.pos_x,ent2.pos_y)

        #print("projectile : ",pos1,ent1.width,ent1.height)
        #print("mob : ",pos2,ent2.width,ent2.height)

        bool_res = self.collision_rec(pos1,ent1.width,ent1.height,pos2,ent2.width,ent2.height)

        return bool_res
    
    def collision_rec(self,center1,width1,height1,center2,width2,height2):

        xleft1,xright1 = center1[0]-width1//2,center1[0]+width1//2
        yleft1,yright1 = center1[1]-height1//2,center1[1]+height1//2

        xleft2,xright2 = center2[0]-width2//2,center2[0]+width2//2
        yleft2,yright2 = center2[1]-height2//2,center2[1]+height2//2

        #print("X : ",xleft1,xright1,xleft2,xright2)
        #print("Y : ",yleft1,yright1,yleft2,yright2)

        if (xleft1<=xright2 and xright1>=xleft2) or (xleft1>=xright2 and xright1<=xleft2):

            if (yleft1<=yright2 and yright1>=yleft2) or (yleft1>=yright2 and yright1<=yleft2) :


                return True
        
        return False
    
    def player_take_damage(self,projectile,player,chunk=99):

        old_pv = player.life
        die = player.take_damage(projectile.damage)
        delta_life = old_pv-player.life
        
        self.effect_send.append([player.id,delta_life,chunk])

        if die:
            print("PLayer is dead")
            self.die_send.append([player.id,chunk,player.die_len])

        projectile.is_dead = True
    
    def add_ent_touch(self,ent,projectile,chunk):

        if ent.id in self.ent_touch :
            self.ent_touch[ent.id][0]+=projectile.damage

        else :
            self.ent_touch[ent.id] = [projectile.damage,projectile.owner,chunk,ent]

    def handle_touch(self,projectile,ent,chunk):

        self.add_ent_touch(ent,projectile,chunk)

        projectile.is_dead = True

    def trigger_ent_touch(self):

        for ent_id,(damage,owner,chunk,ent) in self.ent_touch.items():

            old_pv = ent.life

            die = ent.take_damage(damage,owner)

            delta_life = old_pv-ent.life

            if delta_life!=0:
                self.effect_send.append([ent.id,delta_life,chunk])
            
            if die:
                self.die_send.append([ent.id,chunk,ent.len_dead])

        self.ent_touch.clear()