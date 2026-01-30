class ProjectileManager :

    def __init__(self):
        self.next_id = 0
        self.l_Projectile = []
        self.projectile_create = []
        self.projectile_die = []

    def add_projectile_create(self,projectile):

        projectile.set_id(self.generate_id())

        self.l_Projectile.append(projectile)
        self.projectile_create.append(projectile)

    def add_projectile_when_die(self,lProjectiles,lClient,lProjectiles_create):

        if len(lProjectiles) != 0 :

            for projectile in lProjectiles :

                self.add_projectile_create(projectile)

                self.add_on_client_see_create(lClient,projectile,lProjectiles_create)        

    def generate_id(self):
        self.next_id = (self.next_id+1) % 65536 #Maximum pour uint16
        return self.next_id

    def return_chg(self,lClient,dt,map):

        l = len(lClient)

        projectiles_create = [[] for _ in range(l)]

        for projectile in self.projectile_create :

            self.add_on_client_see_create(lClient,projectile,projectiles_create)

        self.projectile_create.clear()

        projectiles_die = [[] for _ in range(l)]

        for i in range(len(self.l_Projectile)-1,-1,-1) :

            self.l_Projectile[i].move(dt,map)

            if self.l_Projectile[i].should_destroy(map) :

                lProjectiles = self.l_Projectile[i].check_if_projectile_spawn_when_die()
                self.add_projectile_when_die(lProjectiles,lClient,projectiles_create)
                
                self.add_on_client_see_die(lClient,self.l_Projectile[i],projectiles_die)

                del self.l_Projectile[i]

            elif self.l_Projectile[i].to_update :

                self.add_on_client_see_update(lClient,self.l_Projectile[i],projectiles_create)
                self.l_Projectile[i].to_update = False

        infos_shot = []

        for client in lClient.values() :
            infos_shot.append(client.return_next_allowed_shot())
                
        return [projectiles_create,projectiles_die,infos_shot]
    
    def add_on_client_see_create(self,lClient,projectile,projectiles):

        for i,clients in enumerate(lClient.values()):

            if self.client_see(clients,projectile) :

                projectiles[i].append(projectile.return_info())

    def add_on_client_see_update(self,lClient,projectile,projectiles):

        for i,clients in enumerate(lClient.values()):

            if self.client_see(clients,projectile) :

                projectiles[i].append(projectile.return_info())

    def add_on_client_see_die(self,lClient,projectile,projectiles):

        for i,clients in enumerate(lClient.values()):

            if self.client_see(clients,projectile) :
                    
                projectiles[i].append(self.add_when_destroy(projectile))

    def add_when_destroy(self,projectile):
        return projectile.id,int(projectile.pos[0]),int(projectile.pos[1])
    
    def add_when_create(self,projectile):
        return projectile

    def client_see(self,client,projectile):
        return True
