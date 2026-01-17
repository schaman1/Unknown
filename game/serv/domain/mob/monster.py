from serv.domain.mob.mob import Mob
import math

class Monster(Mob):
    def __init__(self, hp, damage, x, y, rad=15, atk_rad=2, atk_speed=1, id = None):

        super().__init__((x,y),hp,id)

        self.hp = hp
        self.damage = damage
        
        self.attack_radius = atk_rad
        self.attack_speed = atk_speed

        self.radius = rad
        
        self.state = "idle"  # idle, moving, attacking, dead

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        
    def distance_to_player(self, lPlayer):
        """Distance euclidienne en cases entre le monstre et le joueur."""
        #return math.sqrt((self.pos_x - Player.pos_x) ** 2 + (self.pos_y - Player.pos_y) ** 2) #Which player ?
        return 5
    
    def is_type(self, type_cell, type_check):
        """
        Vérifie si la cellule est du type spécifié.
        ex: type_check = cell_dur (= [2,5]) -> dur si 2 <= type_cell <= 5
        (DÉPLACÉ depuis Skeleton pour que tous les monstres puissent l'utiliser)
        """
        if type_check[0] <= type_cell <= type_check[1]:
           return True
        return False

    # --- Boucle de comportement basique pour tous les monstres ---

    def update(self, cells_arr, cell_dur, cell_vide, cell_liquid, lPlayer):
        
        if not self.is_alive():
            self.state = "dead"
            return
       
        dist = self.distance_to_player(lPlayer)
        
        if self.state == "idle":
            if dist <= self.radius:
                self.state = "moving"
       
        elif self.state == "moving":
            if dist <= self.attack_radius:
                self.state = "attacking"
            elif dist > self.radius * 1.2:
                self.state = "idle"
               
        elif self.state == "attacking":
            if dist > self.attack_radius:
               # Revenir à l'état de déplacement si le joueur s'éloigne
                self.state = "moving"
            

class Skeleton(Monster):
    def __init__(self, x, y, id):
        super().__init__(hp=50, damage=10, x=x, y=y, rad=10, atk_rad=1.5, atk_speed=1, id=id)

        self.name = 0
        self.direction = 1
        self.idle_min_x = x - 3
        self.idle_max_x = x + 3
    
    #--------------------------------------------------------------------------
    #             --- Deplacements spécifiques au squelette ---
    #--------------------------------------------------------------------------

    def update(self, cells_arr, cell_dur, cell_vide, cell_liquid, lPlayer):
        
        super().update(cells_arr, cell_dur, cell_vide, cell_liquid, lPlayer)
       # --- Deplacement selon l'état ---
        if self.state == "idle":
            self.idle_behavior(cells_arr, cell_dur, cell_vide, cell_liquid)
            
        elif self.state == "moving":
            self.moving_behavior(lPlayer, cells_arr, cell_dur, cell_vide, cell_liquid)
            
        elif self.state == "attacking":
            pass
            #self.attack(lPlayer) #Which player ??
    
    def can_walk_on(self, cells_arr, new_x, new_y, cell_dur, cell_vide, cell_liquid):
        
            # new_x/new_y sont en base_movement -> conversion en indices de case
        bx = int(new_x // self.base_movement)
        by = int(new_y // self.base_movement)

        h = len(cells_arr)
        w = len(cells_arr[0]) if h else 0
            # check si hors map
        if bx < 0 or by < 0 or bx >= w or by >= h:
            return False

        cell_type = cells_arr[by][bx]
        if self.is_type(cell_type, cell_dur):
            return True                                    # peut marcher sur les cellules dures
        if self.is_type(cell_type, cell_liquid):
            return False                                   # ne peut pas marcher sur les liquides
        return True                                        # peux marcher sur les autres cellules (vides, sols)
        
    def idle_behavior(self, cells_arr, cell_dur, cell_vide, cell_liquid):
        next_x = self.pos_x + self.direction * 1
        next_y = self.pos_y                               # on reste sur la même ligne en mode idle
        
       # si on sort de la zone de patrouille ou on tape un mur, on inverse la direction :
        #if (next_x < self.patrol_min_x or next_x > self.patrol_max_x or not self.can_walk_on(cells_arr, next_x, next_y, cell_dur, cell_vide, cell_liquid)):
        #    self.direction *= -1
        #    next_x = self.pos_x + self.direction * 0.05    # recalculer la prochaine position après inversion
       
       # déplacement si la case est autorisée
        if self.can_walk_on(cells_arr, next_x, next_y, cell_dur, cell_vide, cell_liquid):
            self.pos_x = next_x
           
    def moving_behavior(self, lPlayer, cells_arr, cell_dur, cell_vide, cell_liquid):
       # Déterminer la direction vers le joueur
        #if Player.pos_x > self.pos_x: #Changer car existe plus que 1 joueur
        #    self.direction = 1
        #elif Player.pos_x < self.pos_x:
        #    self.direction = -1
        next_x = self.pos_x + self.direction * 1
        next_y = self.pos_y
       # on réutilise la même logique de collision
        if self.can_walk_on(cells_arr, next_x, next_y, cell_dur, cell_vide, cell_liquid):
            self.pos_x = next_x
       
    def attack(self, lPlayer):
       # Inflige des dégâts au joueur en fonction de la vitesse d'attaque
        for _ in range(self.attack_speed):
            lPlayer.take_damage(self.damage)
        