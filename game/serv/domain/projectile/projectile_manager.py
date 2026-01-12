from serv.domain.projectile import weapon

class ProjectileManager :

    def __init__(self):
        self.next_id = 0
        self.l_Projectile = []
        self.projectile_create = []
        self.projectile_die = []

    def generate_id(self):
        self.next_id = (self.next_id+1) % 65536 #Maximum pour uint16
        return self.next_id
    
    def create_shoot(self,type_weapon,angle,pos):
        
        if type_weapon == "pioche" :
            projectile = weapon.Pioche(self.generate_id(),angle,pos) #0 = pioche
            self.l_Projectile.append(projectile)
            self.projectile_create.append(projectile)
        else :
            print("Unknown weapon")

    def return_chg(self,lClient,dt):

        l = len(lClient)

        projectiles_create = [[] for _ in range(l)]

        for projectile in self.projectile_create :

            self.add_on_client_see_create(lClient,projectile,projectiles_create)

        self.projectile_create.clear()

        projectiles_die = [[] for _ in range(l)]
        
        for i in range(len(self.l_Projectile)-1,-1,-1) :

            self.l_Projectile[i].move(dt)

            if self.l_Projectile[i].should_destroy() :
                
                self.add_on_client_see_die(lClient,self.l_Projectile[i],projectiles_die)

                del self.l_Projectile[i]
                
        return [projectiles_create,projectiles_die]
    
    def add_on_client_see_create(self,lClient,projectile,projectiles):

        for i,clients in enumerate(lClient.values()):

            if self.client_see(clients,projectile) :

                projectiles[i].append(projectile.return_info())

    def add_on_client_see_die(self,lClient,projectile,projectiles):

        for i,clients in enumerate(lClient.values()):

            if self.client_see(clients,projectile) :
                    
                projectiles[i].append(self.add_when_destroy(projectile))

    def add_when_destroy(self,projectile):
        return projectile.id
    
    def add_when_create(self,projectile):
        return projectile

    def client_see(self,client,projectile):
        return True
