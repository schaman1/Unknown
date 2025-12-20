import math
from serv.in_game.Mob.C_mob import Mob

class Monster(Mob):
    def __init__(self, hp, damage, x, y, rad=15, atk_rad=2, atk_speed=1, id = None):

        super().__init__((x,y),hp,id)

        self.hp = hp
        self.damage = damage
        
        self.attack_radius = atk_rad
        self.attack_speed = atk_speed
        
        self.state = "idle"  # idle, moving, attacking, dead

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        
    #def distance_to_player(self, Player):
        """Distance euclidienne en cases entre le monstre et le joueur."""
    #    return math.sqrt((self.pos_x - Player.pos_x) ** 2 + (self.pos_y - Player.pos_y) ** 2)
    
    #def is_type(self, type_cell, type_check):
        """
        Vérifie si la cellule est du type spécifié.
        ex: type_check = cell_dur (= [2,5]) -> dur si 2 <= type_cell <= 5
        (DÉPLACÉ depuis Skeleton pour que tous les monstres puissent l'utiliser)
        """
    #    if type_check[0] <= type_cell <= type_check[1]:
    #       return True
    #    return False
    
    # --- Boucle de comportement basique pour tous les monstres ---
    
    #def update(self, cells_arr, cell_dur, cell_vide, cell_liquid, Player):
    #    if not self.is_alive():
    #        self.state = "dead"
    #        return
        
    #    dist = self.distance_to_player(Player)
    #    
    #    if self.state == "idle":
    #        if dist <= self.radius:
    #            self.state = "moving"
        
    #    elif self.state == "moving":
    #        if dist <= self.attack_radius:
    #            self.state = "attacking"
    #        elif dist > self.radius * 1.2:
    #            self.state = "idle"
                
    #    elif self.state == "attacking":
    #        if dist > self.attack_radius:
                # Revenir à l'état de déplacement si le joueur s'éloigne
    #            self.state = "moving"
                
        # --- Deplacement selon l'état ---
    #    if self.state == "idle":
    #        self.idle_behavior(cells_arr, cell_dur, cell_vide, cell_liquid)
            
    #    elif self.state == "moving":
    #        self.moving_behavior(Player, cells_arr, cell_dur, cell_vide, cell_liquid)
         
    #    elif self.state == "attacking":
    #        self.attack(Player)

class Skeleton(Monster):
    def __init__(self, x, y, id):
        
        super().__init__(hp=50, damage=10, x=x, y=y, rad=10, atk_rad=1.5, atk_speed=1, id = id)
        
        self.name = 0 #:"Skeleton"

        self.direction = 1        # 1 = va vers la droite, -1 = vers la gauche
        self.idle_min_x = x - 3   # borne gauche de patrouille (idle) (3 cases autour de la position de spawn)
        self.idle_max_x = x + 3   # borne droite
    
    #--------------------------------------------------------------------------
    #             --- Deplacements spécifiques au squelette ---
    #--------------------------------------------------------------------------

    def move(self,cells_arr,cell_dur,cell_vide,cell_liquid): #Appele a chaque iteration mais pourra changer après
        return (0,0)
    
    def can_walk_on(self, cells_arr, cell_dur, cell_vide, cell_liquid, new_x, new_y):
        cell_type = cells_arr[int(new_y)][int(new_x)]
        
        if self.is_type(cell_type, cell_dur):              #ne peux pas marcher sur les cellules dures
            return False
        if self.is_type(cell_type, cell_liquid):           #ne peux pas marcher sur les liquides
            return False
        return True                                        # peux marcher sur les autres cellules (vides, sols)
        
    #def idle_behavior(self, cells_arr, cell_dur, cell_vide, cell_liquid):
    #    next_x = self.pos_x + self.direction * 0.05        # vitesse de patrouille en mode idle
    #    next_y = self.pos_y                                # on reste sur la même ligne en mode idle
        
        # si on sort de la zone de patrouille ou on tape un mur, on inverse la direction :
    #    if (next_x < self.patrol_min_x or next_x > self.patrol_max_x or not self.can_walk_on(cells_arr, next_x, next_y, cell_dur, cell_vide, cell_liquid)):
    #        self.direction *= -1
    #        next_x = self.pos_x + self.direction * 0.05    # recalculer la prochaine position après inversion
        
        # déplacement si la case est autorisée
    #    if self.can_walk_on(cells_arr, next_x, next_y, cell_dur, cell_vide, cell_liquid):
    #        self.pos_x = next_x
            
            
    #def moving_behavior(self, Player, cells_arr, cell_dur, cell_vide, cell_liquid):
        # Déterminer la direction vers le joueur
    #    if Player.pos_x > self.pos_x:
    #        self.direction = 1
    #    elif Player.pos_x < self.pos_x:
    #        self.direction = -1

    #    next_x = self.pos_x + self.direction
    #    next_y = self.pos_y

        # on réutilise la même logique de collision
    #    if self.can_walk_on(cells_arr, next_x, next_y, cell_dur, cell_vide, cell_liquid):
    #        self.pos_x = next_x
        
        
    #def attack(self, Player):
        # Inflige des dégâts au joueur en fonction de la vitesse d'attaque
    #    for _ in range(self.attack_speed):
    #        Player.take_damage(self.damage)
        