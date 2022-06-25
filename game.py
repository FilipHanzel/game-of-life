import random


class Game:
    __slots__ = ("map", "size")

    def __init__(self, size: int = 100):
        self.map = [[0] * size for _ in range(size)]
        self.size = size

    def _count_living_neighbors(self, row_idx: int, col_idx: int) -> int:
        count = 0

        row_prev = row_idx - 1
        col_prev = col_idx - 1
        row_next = (row_idx + 1) % self.size
        col_next = (col_idx + 1) % self.size

        count += self.map[row_prev][col_prev]
        count += self.map[row_prev][col_idx]
        count += self.map[row_prev][col_next]
        count += self.map[row_idx][col_prev]
        count += self.map[row_idx][col_next]
        count += self.map[row_next][col_prev]
        count += self.map[row_next][col_idx]
        count += self.map[row_next][col_next]

        return count

    def _get_new_cell_state(self, row_idx: int, col_idx: int) -> int:
        neighbors = self._count_living_neighbors(row_idx, col_idx)
        current_state = self.map[row_idx][col_idx]

        if current_state == 0 and neighbors == 3:
            return 1
        if current_state == 1 and neighbors not in (2, 3):
            return 0
        return current_state

    def update(self):
        self.map = [
            [self._get_new_cell_state(row_idx, col_idx) for col_idx in range(self.size)]
            for row_idx in range(self.size)
        ]

    def randomize(self):
        self.map = [
            [random.randint(0, 1) for _ in range(self.size)] for _ in range(self.size)
        ]
