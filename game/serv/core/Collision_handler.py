from serv.domain.mob.team import Team

class CollisionHandler:

    def __init__(self):
        self.effect_send = []

    def trigger_collision(self,mobs,players,projectiles):

        for chunk,l_projectile in projectiles.items() : 

            for projectile in l_projectile:

                if projectile.team!=Team.Player:

                    for player in players.values() :

                        touch = self.collision(projectile,player)

                        if touch :
                            #print("Player touch")
                            self.handle_touch(projectile,player,chunk)
                        
                if projectile.team!=Team.Mob:

                    for mob in mobs[chunk] :


                        touch = self.collision(projectile,mob)

                        if touch :
                            #print("Mob touch")
                            self.handle_touch(projectile,mob,chunk)


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

        print("X : ",xleft1,xright1,xleft2,xright2)
        print("Y : ",yleft1,yright1,yleft2,yright2)

        if xleft1<=xright2 or xright1<=xleft2 :

            if yleft1<=yright2 or yright1<=yleft2 :


                return True
        
        return False

    def handle_touch(self,projectile,ent,chunk):
        old_pv = ent.life
        ent.take_damage(projectile.damage)
        delta_life = old_pv-ent.life

        self.effect_send.append([ent.id,delta_life,chunk])

        projectile.is_dead = True