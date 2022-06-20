import time
from entities.towers.tower import Tower
from entities.towers.projectile import Projectile


class BombTower(Tower):
    """
    Der Bomben-Turm.
    """
    cost = 10

    def __init__(self, _pos: tuple):
        _symbol_path = "assets/img/towers/bomb_1.png"
        _range = 150
        _cool_down = 3.0
        _attack_power = 1

        _cost = BombTower.cost
        super().__init__(_pos, _symbol_path, _range, _cool_down, _attack_power, _cost)

        self.projectiles = list()
        self.position_to_attack = (0, 0)

    def attack(self):
        """
        Instanziert ein Projektil der Klasse Projektil, wenn ein Gegner in Reichweite ist. Das Projektil wird auf die
        aktuelle Position des Gegners gezielt und in die Liste der aktiven Projektile eingefügt.
        :return: boolean: True, fals ein Projektil instanziert wurde. False falls nicht.
        """
        if self.active:
            if time.time() - self.timer >= self.cool_down_time:
                self.timer = time.time()
                self.position_to_attack = self.aimed_enemy.get_center()

                projectile = Projectile(self.center, self.position_to_attack,
                                        self.attack_power, self.attack_power_level)
                self.projectiles.append(projectile)
                return True
        return False

    def draw_attack(self, win):
        """
        Durchläuft die Liste der aktiven Projektile und zeichnet deren Symbole auf das Window.
        :param win: Das aktuelle Window.
        :return:
        """
        for projectile in self.projectiles:
            projectile.draw_projectile(win)

    def get_impacted_projectiles(self):
        """
        Durchläuft die Liste der aktiven Projektile. Wenn ein Projektil den Status 'impacted' hält, wird es aus der
        Liste entfernt und in die Liste der impacted projectiles eingefügt.
        :return: list: impacted projetiles.
        """
        impacted_projectiles = list()
        for projectile in self.projectiles:
            if projectile.is_impacted():
                impacted_projectiles.append(projectile)
        for impacted in impacted_projectiles:
            self.projectiles.remove(impacted)
        return impacted_projectiles

    def upgrade_speed(self):
        """
        Erhöht die Angriffsgeschwindigkeit und die Kosten dafür.
        :return: True: wenn upgrade erfolgreich, False, wenn nicht.
        """
        if self.speed_level < 10:
            self.speed_upgrade_cost += 4 * self.fibonacci(self.speed_level)
            self.cool_down_time -= 0.15
            self.speed_level += 1
            return True
        return False

    def increase_cost(self):
        """
        Erhöht die Baukosten um 1
        :return:
        """
        BombTower.cost += 1

    def decrease_cost(self):
        """
        Verringert die Baukosten um 1
        :return:
        """
        BombTower.cost -= 1

    def redeem_coins(self):
        """
        Verringert die Baukosten um 1.
        :return:
        """
        return BombTower.cost - 1
