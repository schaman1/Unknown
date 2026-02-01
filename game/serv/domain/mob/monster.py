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
        
    def distance_to_nearest_player(self, lPlayer):
        """Distance euclidienne en cases entre le monstre et le joueur."""
        target = None
        best = None
        for p in lPlayer.values():
            dx = p.pos_x - self.pos_x
            dy = p.pos_y - self.pos_y
            d = math.hypot(dx, dy)
            if best is None or d < best:
                best = d
                target = p
        if target is None:
            return None, float("inf")
        return target, best / self.base_movement

    # --- Boucle de comportement basique pour tous les monstres ---

    def update(self, map,lPlayer):
        
        if not self.is_alive():
            self.state = "dead"
            return

        target, dist = self.distance_to_nearest_player(lPlayer)

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
            elif dist <= self.attack_radius:
                # Attaquer le joueur
                 self.attack(target)

    # --- Déplacement pour gestion des collisions ---

    # Vérifie si une cellule est bloquante (dure ou liquide)
    def is_blocking_cell(self, cell_type, cell_dur, cell_liquid):
        return self.is_type(cell_type, cell_dur) or self.is_type(cell_type, cell_liquid)

    # Essayer de déplacer le monstre selon l'axe X en gérant les collisions
    def try_move_axis_x(self, dx, cells_arr, cell_dur, cell_liquid):
        if dx == 0:
            return 0

        s = -1 if dx < 0 else 1
        remaining = abs(dx)
        moved = 0

        while remaining > 0:
            step = min(self.base_movement, remaining)
            next_x = self.pos_x + s * step

            x_check = next_x + (self.half_width + self.base_movement) * s
            y_top = self.pos_y - self.half_height
            y_bottom = self.pos_y + self.half_height

            ok = True
            y = y_top
            while y <= y_bottom:
                bx = self.convert_to_base(x_check)
                by = self.convert_to_base(y)

                if by < 0 or by >= cells_arr.shape[0] or bx < 0 or bx >= cells_arr.shape[1]:
                    ok = False
                    break

                if self.is_blocking_cell(int(cells_arr[by, bx]), cell_dur, cell_liquid):
                    ok = False
                    break

                y += self.base_movement

            if not ok:
                break

            self.pos_x = next_x
            moved += s * step
            remaining -= step

        return moved

    # Essayer de déplacer le monstre selon l'axe Y en gérant les collisions
    def try_move_axis_y(self, dy, cells_arr, cell_dur, cell_liquid):
        if dy == 0:
            return 0

        s = -1 if dy < 0 else 1
        remaining = abs(dy)
        moved = 0

        while remaining > 0:
            step = min(self.base_movement, remaining)
            next_y = self.pos_y + s * step

            y_check = next_y + (self.half_height + self.base_movement) * s
            x_left = self.pos_x - self.half_width
            x_right = self.pos_x + self.half_width

            ok = True
            x = x_left
            while x <= x_right:
                bx = self.convert_to_base(x)
                by = self.convert_to_base(y_check)

                if by < 0 or by >= cells_arr.shape[0] or bx < 0 or bx >= cells_arr.shape[1]:
                    ok = False
                    break

                if self.is_blocking_cell(int(cells_arr[by, bx]), cell_dur, cell_liquid):
                    ok = False
                    break

                x += self.base_movement

            if not ok:
                break

            self.pos_y = next_y
            moved += s * step
            remaining -= step

        return moved
    
    # Vérifie si le monstre chevauche une cellule dure
    def overlaps_dur(self,map):
        i = -self.half_height
        while i <= self.half_height:
            j = -self.half_width
            while j <= self.half_width:
                if self.touch_wall(i, j,map):
                    return True
                j += self.base_movement
            i += self.base_movement
        return False

    # Essayer de monter d'une cellule si possible lors d'un déplacement horizontal
    def try_step_up_1(self,map, intended_vx,dt):
        if intended_vx == 0:
            return 0

        if not self.touch_ground(map):
            return 0

        old_x = self.pos_x
        old_y = self.pos_y
        old_vx = self.vitesse_x

        self.pos_y = old_y - self.base_movement
        if self.overlaps_dur(map):
            self.pos_x = old_x
            self.pos_y = old_y
            self.vitesse_x = old_vx
            return 0
        self.vitesse_x = intended_vx
        moved = self.collision_x(map,dt)

        if moved == 0:
            self.pos_x = old_x
            self.pos_y = old_y
            self.vitesse_x = old_vx
            return 0
        return moved


#Creation d'un monstre spécifique : le squelette

class Skeleton(Monster):
    def __init__(self, x, y, id):
        super().__init__(hp=50, damage=10, x=x, y=y, rad=30, atk_rad=5, atk_speed=1, id=id)

        self.name = 0
        
        #idle state preset, peux chnanger selon le monstre
        self.direction = 1
        self.idle_min_x = x - 30 *self.base_movement
        self.idle_max_x = x + 30 *self.base_movement
        
        #diffent speed selon l'etat
        self.speed_idle = max(1, self.base_movement * 8)
        self.speed_chase = max(1, self.base_movement * 5)
        self.speed_max = max(1, self.base_movement * 6)
        
        #pour le stepup et le no turn lors de l'idle
        self.step_lock = 0
        self.no_turn = 0
        self.idle_stuck = 0

    def update(self, map, lPlayer,dt):
        
        super().update(map,lPlayer)
       # --- Deplacement selon l'état ---
        if self.state == "idle":
            self.idle_behavior(map,dt)
            
        elif self.state == "moving":
            self.moving_behavior(lPlayer, map,dt)
            
        elif self.state == "attacking":
            pass
    
    def can_walk_on(self, cells_arr, new_x, new_y, cell_dur, cell_vide, cell_liquid):
        
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
        
        #--- Comportements spécifiques ---
        
    #comportement en mode idle : patrouille entre deux points fixes
    def idle_behavior(self, map,dt):
        intended_vx = self.direction * self.speed_idle
        if intended_vx == 0:
            intended_vx = self.direction * max(1, self.base_movement // 8)

        if self.pos_x + intended_vx < self.idle_min_x or self.pos_x + intended_vx > self.idle_max_x:
            self.direction *= -1
            intended_vx = self.direction * max(1, self.base_movement // 8)

        self.gravity_effect()
        self.vitesse_x = intended_vx
        moved_x = self.collision_x(map,dt)
        self.collision_y(map,dt)

        if moved_x == 0 and intended_vx != 0:
            stepped = self.try_step_up_1(map, intended_vx,dt)
            if stepped != 0:
                self.step_lock = 4
                self.no_turn = 6
                moved_x = stepped
                self.vitesse_x = intended_vx
                self.collision_x(map,dt)
            self.collision_y(map,dt)

        if moved_x == 0:
            self.idle_stuck += 1
        else:
            self.idle_stuck = 0

        if self.step_lock > 0:
            self.step_lock -= 1
        if self.no_turn > 0:
            self.no_turn -= 1

        if moved_x == 0:
            if self.idle_stuck >= 10:
                self.direction *= -1
                self.idle_stuck = 0
                self.no_turn = 0
                self.step_lock = 0
            elif self.no_turn == 0 and self.step_lock == 0:
                self.direction *= -1
                
    # comportement en mode moving : poursuite du joueur le plus proche      
    def moving_behavior(self, lPlayer, map,dt):
        target, _ = self.distance_to_nearest_player(lPlayer)

        #print("Here")

        if target is None:
            return

        dx = target.pos_x - self.pos_x
        if abs(dx) < self.base_movement // 10:
            intended_vx = 0
        else:
            intended_vx = self.speed_max if dx > 0 else -self.speed_max

        self.gravity_effect()
        self.vitesse_x = intended_vx
        moved_x = self.collision_x(map,dt)
        self.collision_y(map,dt)
        
        if moved_x == 0 and intended_vx != 0:
            stepped = self.try_step_up_1(map, intended_vx,dt)
            if stepped != 0:
                self.step_lock = 4
                self.no_turn = 6
                moved_x = stepped
                self.vitesse_x = intended_vx
                self.collision_x(map,dt)
            self.collision_y(map,dt)
        
        if self.step_lock > 0:
            self.step_lock -= 1

        if self.no_turn > 0:
            self.no_turn -= 1
            
        if intended_vx != 0:
            self.direction = 1 if intended_vx > 0 else -1
            
    # attaque le joueur le plus proche    
    def attack(self, lPlayer):
       # Inflige des dégâts au joueur en fonction de la vitesse d'attaque
        for _ in range(self.attack_speed):
            lPlayer.take_damage(self.damage)