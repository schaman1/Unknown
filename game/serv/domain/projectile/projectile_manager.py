from shared.constants.world import LEN_X_CHUNK,LEN_Y_CHUNK

class ProjectileManager :

    def __init__(self,width_chunk,height_chunk):
        self.size_chunk_all = (LEN_Y_CHUNK,LEN_X_CHUNK)
        self.size_chunk = (height_chunk,width_chunk)

        self.next_id = 0
        self.dic_projectiles = {}
        self.projectile_create = []
        self.projectile_die = []

        self.init_dic_projectiles()

    def init_dic_projectiles(self) :

        for i in range(self.size_chunk_all[0]) :
            for j in range(self.size_chunk_all[1]) :
                self.dic_projectiles[i*100+j] = []

    def add_projectile_create(self,projectile):

        projectile.set_id(self.generate_id())

        chunk = self.calculate_chunk(projectile)

        self.dic_projectiles[chunk].append(projectile)
        self.projectile_create.append(projectile)

    def calculate_chunk(self,projectile):
        """Return the chunk in which the projectile curently is"""

        chunk_x = projectile.pos_x//self.size_chunk[1]//100
        chunk_y = projectile.pos_y//self.size_chunk[0]//100

        return chunk_y*100+chunk_x

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

        for l_projectile in self.dic_projectiles.values() :

            for i in range(len(l_projectile)-1,-1,-1) :

                l_projectile[i].move(dt,map)

                if l_projectile[i].should_destroy(map) :

                    lProjectiles = l_projectile[i].check_if_projectile_spawn_when_die()
                    self.add_projectile_when_die(lProjectiles,lClient,projectiles_create)
                    
                    self.add_on_client_see_die(lClient,l_projectile[i],projectiles_die)

                    del l_projectile[i]

                elif l_projectile[i].to_update :

                    self.add_on_client_see_update(lClient,l_projectile[i],projectiles_create)
                    l_projectile[i].to_update = False

        infos_shot = []

        for client in lClient.values() :
            infos_shot.append(client.return_next_allowed_shot())
        #print("infos_shot",infos_shot)
                
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
        return projectile.id,int(projectile.pos_x),int(projectile.pos_y)
    
    def add_when_create(self,projectile):
        return projectile

    def client_see(self,client,projectile):
        return True
