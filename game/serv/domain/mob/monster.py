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

    def is_blocking_cell(self, cell_type, cell_dur, cell_liquid):
        return self.is_type(cell_type, cell_dur) or self.is_type(cell_type, cell_liquid)


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

class Skeleton(Monster):
    def __init__(self, x, y, id):
        super().__init__(hp=50, damage=10, x=x, y=y, rad=10, atk_rad=1.5, atk_speed=1, id=id)

        self.name = 0
        self.direction = 1
        self.idle_min_x = x - 3 *self.base_movement
        self.idle_max_x = x + 3 *self.base_movement
        self.speed_idle = max(1, self.base_movement // 8)
        self.speed_chase = max(1, self.base_movement // 5)

    def update(self, cells_arr, cell_dur, cell_vide, cell_liquid, lPlayer):
        
        super().update(cells_arr, cell_dur, cell_vide, cell_liquid, lPlayer)
       # --- Deplacement selon l'état ---
        if self.state == "idle":
            self.idle_behavior(cells_arr, cell_dur, cell_vide, cell_liquid)
            
        elif self.state == "moving":
            self.moving_behavior(lPlayer, cells_arr, cell_dur, cell_vide, cell_liquid)
            
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
        
    def idle_behavior(self, cells_arr, cell_dur, cell_vide, cell_liquid):
        dx = self.direction * self.speed_idle
        next_x = self.pos_x + dx
        
        out_patrol = next_x < self.idle_min_x or next_x > self.idle_max_x
        if out_patrol :
            self.direction *= -1
            dx = self.direction * self.speed_idle

        moved = self.try_move_axis_x(dx, cells_arr, cell_dur, cell_liquid)
        if moved == 0:
            self.direction *= -1
           
    def moving_behavior(self, lPlayer, cells_arr, cell_dur, cell_vide, cell_liquid):
        target, _ = self.distance_to_nearest_player(lPlayer)
        if target is None:
            return

        dx = target.pos_x - self.pos_x
        dy = target.pos_y - self.pos_y
        
        step_x = 0
        step_y = 0
        if abs(dx) > 0:
            step_x = self.speed_chase if dx > 0 else -self.speed_chase
        if abs(dy) > 0:
            step_y = self.speed_chase if dy > 0 else -self.speed_chase
            
        moved = 0
        if abs(dx) >= abs(dy):
            moved = self.try_move_axis_x(step_x, cells_arr, cell_dur, cell_liquid)
            if moved == 0:
                self.try_move_axis_y(step_y, cells_arr, cell_dur, cell_liquid)
        else:
            moved = self.try_move_axis_y(step_y, cells_arr, cell_dur, cell_liquid)
            if moved == 0:
                self.try_move_axis_x(step_x, cells_arr, cell_dur, cell_liquid)

        if step_x != 0:
            self.direction = 1 if step_x > 0 else -1
        
    def attack(self, lPlayer):
       # Inflige des dégâts au joueur en fonction de la vitesse d'attaque
        for _ in range(self.attack_speed):
            lPlayer.take_damage(self.damage)
        