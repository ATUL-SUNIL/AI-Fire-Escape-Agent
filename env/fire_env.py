import numpy as np
import random
from collections import deque

class FireEscapeEnv:
    def __init__(self, size=(10, 10), fire_spread_chance=0.2):
        self.size = size
        self.grid = np.zeros(size, dtype=int)
        self.agent_pos = (0, 0)
        # 3 exits in corners
        self.exit_positions = [(size[0]-1, size[1]-1), (0, size[1]-1), (size[0]-1, 0)]
        self.fire_spread_chance = fire_spread_chance
        self.reset()

    def reset(self):
        while True:
            self.grid.fill(0)
            self.agent_pos = (0, 0)

            for exit_pos in self.exit_positions:
                self.grid[exit_pos] = 3
            self.grid[self.agent_pos] = 4

            # add walls randomly
            wall_count = int(self.size[0] * self.size[1] * 0.2)
            for _ in range(wall_count):
                i, j = random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1)
                if (i, j) != self.agent_pos and (i, j) not in self.exit_positions:
                    self.grid[i][j] = 1

            # place only 1 fire to start
            self.place_fire()

            # check if atleast one exit is reachable
            if self._is_exit_reachable():
                break

    def place_fire(self):
        # place fire on random empty cell
        empty_cells = [
            (i, j) for i in range(1, self.size[0] - 1)
                   for j in range(1, self.size[1] - 1)
                   if self.grid[i][j] == 0 and (i, j) != self.agent_pos and (i, j) not in self.exit_positions
        ]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2

    def _is_exit_reachable(self):
        visited = set()
        q = deque([self.agent_pos])

        while q:
            x, y = q.popleft()
            if (x, y) in self.exit_positions:
                return True
            # bfs to find exit
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size[0] and 0 <= ny < self.size[1]:
                    if self.grid[nx][ny] in [0, 3] and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        q.append((nx, ny))
        return False

    def spread_fire(self):
        new_fire = []
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.grid[i][j] == 2:
                    # fire spreads to neighbours randomly
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            ni, nj = i + dx, j + dy
                            if 0 <= ni < self.size[0] and 0 <= nj < self.size[1]:
                                if self.grid[ni][nj] == 0 and random.random() < self.fire_spread_chance:
                                    new_fire.append((ni, nj))
        for pos in new_fire:
            self.grid[pos] = 2

    def move_agent(self, new_pos):
        # check valid move
        if not (0 <= new_pos[0] < self.size[0] and 0 <= new_pos[1] < self.size[1]):
            return False
        if self.grid[new_pos] in [1, 2]:
            return False
        self.grid[self.agent_pos] = 0
        self.agent_pos = new_pos
        self.grid[new_pos] = 4
        return True

    def is_exit_reached(self):
        return self.agent_pos in self.exit_positions

    def is_agent_dead(self):
        return self.grid[self.agent_pos] == 2

    def render(self):
        # print grid for testing
        print(self.grid)
