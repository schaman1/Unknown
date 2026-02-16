from serv.domain.mob.team import Team

class CollisionHandler:

    def __init__(self):
        pass

    def trigger_collision(self,mobs,players,projectiles):

        for chunk,l_projectile in projectiles.items() : 

            for projectile in l_projectile:

                if projectile.team==Team.Player:

                    for player in players.values() :

                        touch = self.collision(projectile,player)

                        if touch :
                            print("Touch")
                            self.handle_touch(projectile,player)
                        
                if projectile.team!=Team.Mob:

                    for mob in mobs[chunk] :

                        touch = self.collision(projectile,mob)

                        if touch :
                            self.handle_touch(projectile,mob)


    def collision(self,ent1,ent2):

        return True
    
    def handle_touch(self,projectile,ent):
        ent.take_damage(projectile.damage)

        projectile.is_dead = True