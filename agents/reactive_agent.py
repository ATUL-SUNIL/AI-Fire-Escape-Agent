import random

class ReactiveAgent:
    def __init__(self, env):
        self.env = env

    def get_valid_moves(self):
        x, y = self.env.agent_pos
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.env.size[0] and 0 <= ny < self.env.size[1]:
                if self.env.grid[nx][ny] in [0, 3]:  # Empty or Exit
                    moves.append((nx, ny))

        return moves

    def choose_move(self):
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return None
        # Prefer move toward exit
        # Choose closest of all safe exits
        exit_positions = [pos for pos in self.env.exit_positions if self.env.grid[pos] == 3]
        if not exit_positions:
            return valid_moves[0]  # no safe exit, just pick something

        valid_moves.sort(key=lambda move: min(self.manhattan_distance(move, ex) for ex in exit_positions))

        return valid_moves[0]

    def manhattan_distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
