from entities.enemies.enemy import Enemy


class EnemyTwo(Enemy):
    """
    Stärkste Gegner-Klasse.
    """
    def __init__(self, _path):
        symbol_path = "assets/img/enemies/enemy_2.png"
        hp = 16
        level = 2
        super().__init__(_path, hp, symbol_path, level)
