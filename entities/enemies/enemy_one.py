from entities.enemies.enemy import Enemy


class EnemyOne(Enemy):
    """
    Schwächste Gegner-Klasse.
    """
    def __init__(self, _path):
        symbol_path = "assets/img/enemies/enemy_1.png"
        hp = 10
        level = 1
        super().__init__(_path, hp, symbol_path, level)

