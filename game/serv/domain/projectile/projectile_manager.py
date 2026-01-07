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
            self.projectile_create.append(projectile.return_info())
        else :
            print("Unknown weapon")

    def return_chg(self,lClient,dt):

        l = len(lClient)

        projectiles_create = [[] for _ in range(l)]

        for projectile in self.projectile_create :

            self.add_on_client_see(lClient,l,projectile,projectiles_create,"Create")

        self.projectile_create.clear()

        projectiles_die = [[] for _ in range(l)]
        
        for i in range(len(self.l_Projectile)-1,-1,-1) :

            self.l_Projectile[i].move(dt)

            if self.l_Projectile[i].should_destroy() :
                
                self.add_on_client_see(lClient,l,self.l_Projectile[i],projectiles_die,"Die")

                del self.l_Projectile[i]
                
                #comment faire de maniere opti la de supprimer ce projectile de l_self.lProjectile

        return [projectiles_create,projectiles_die]

    def add_on_client_see(self,lClient,len_clients,projectile,projectiles,state):


        for i,clients in enumerate(lClient.values()):

            if self.client_see(clients,projectile) :
                if state == "Die" :
                    projectiles[i].append(self.add_when_destroy(projectile))

                elif state == "Create" :
                    projectiles[i].append(self.add_when_create(projectile))


    def add_when_destroy(self,projectile):
        return projectile.id
    
    def add_when_create(self,projectile):
        return projectile

    def client_see(self,client,projectile):
        return True
