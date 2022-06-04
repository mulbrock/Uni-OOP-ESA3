from entities.enemies.enemy import Enemy

class EnemyThree(Enemy):

    def __init__(self, _path):
        symbol_path = "assets/img/enemies/enemy_3.png"
        hp = 20
        level = 3
        super().__init__(_path, hp, symbol_path, level)
