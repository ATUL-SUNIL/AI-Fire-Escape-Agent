import heapq

class SearchAgent:
    def __init__(self, env):
        self.env = env

    def manhattan_distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, pos):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dx, dy in directions:
            nx, ny = pos[0] + dx, pos[1] + dy
            if 0 <= nx < self.env.size[0] and 0 <= ny < self.env.size[1]:
                if self.env.grid[nx][ny] in [0, 3]:  # empty or exit
                    neighbors.append((nx, ny))
        return neighbors

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def find_path(self):
        start = self.env.agent_pos
        goals = [pos for pos in self.env.exit_positions if self.env.grid[pos] == 3]  # only unburned exits

        if not goals:
            return []

        # Find the goal with the lowest manhattan distance
        goals.sort(key=lambda g: self.manhattan_distance(start, g))
        goal = goals[0]  # pick nearest safe exit

        open_set = []
        heapq.heappush(open_set, (0 + self.manhattan_distance(start, goal), 0, start))

        came_from = {}
        g_score = {start: 0}

        while open_set:
            _, cost, current = heapq.heappop(open_set)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.manhattan_distance(neighbor, goal)
                    heapq.heappush(open_set, (f_score, tentative_g_score, neighbor))

        return []

    def next_move(self):
        path = self.find_path()
        if len(path) >= 2:
            return path[1]  # next step
        else:
            return None
