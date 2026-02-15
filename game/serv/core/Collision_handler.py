

class CollisionHandler:

    def __init__(self):
        pass

    def trigger_collision(self,mobs,players,projectiles):

        return

        for projectile in projectiles : 

            if projectile.can_damage == "player" or projectile.can_damage == "all":

                for player in players.values() :

                    touch = self.collision(projectile,player)

                    if touch :
                        self.handle_touch(projectile,player)
                    
            if projectile.can_damage == "mob" or projectile.can_damage == "all":

                for mob in mobs.values() :

                    touch = self.collision(projectile,mob)

                    if touch :
                        self.handle_touch(projectile,mob)