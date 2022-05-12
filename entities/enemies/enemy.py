import math
from entities.entity import Entity


class Enemy(Entity):

    def __init__(self, _size: tuple, _path, _hp, _symbol):
        super().__init__(_size, _path[0], _symbol)

        self.max_hp = _hp
        self.hp = _hp

        self.path = _path
        self.path_stage = 0

        self.step_count = 0

    def move_forward(self):
        x1, y1 = self.get_pos()

        if self.path_stage + 1 < len(self.path):
            x2, y2 = self.path[self.path_stage + 1]
        else:
            return False

        dir_vector = ((x2 - x1) * 2, (y2 - y1) * 2)
        dir_vector_length = math.sqrt((dir_vector[0]) ** 2 + (dir_vector[1]) ** 2)
        dir_vector = (dir_vector[0] / dir_vector_length, dir_vector[1] / dir_vector_length)

        step = ((x1 + dir_vector[0]), (y1 + dir_vector[1]))

        self.set_pos((step[0], step[1]))
        x1, y1 = self.get_pos()

        if dir_vector[0] >= 0:
            if dir_vector[1] >= 0:
                if x1 >= x2 and y1 >= y2:
                    self.path_stage += 1
            else:
                if x1 >= x2 and y1 <= y2:
                    self.path_stage += 1
        else:
            if dir_vector[1] >= 0:
                if x1 <= x2 and y1 >= y2:
                    self.path_stage += 1
            else:
                if x1 <= x2 and y1 >= y2:
                    self.path_stage += 1

        return True

