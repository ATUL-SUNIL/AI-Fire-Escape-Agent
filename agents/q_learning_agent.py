import random
import numpy as np
import pickle

class QLearningAgent:
    def __init__(self, env, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.env = env
        self.q_table = {}
        self.alpha = alpha  # learning rate
        self.gamma = gamma  # discount factor
        self.epsilon = epsilon  # exploration rate
        self.actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

    def save_q_table(self, filename="q_table.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.q_table, f)
        print(f"✅ Q-table saved to {filename}")

    def load_q_table(self, filename="q_table.pkl"):
        try:
            with open(filename, "rb") as f:
                self.q_table = pickle.load(f)
            print(f"📂 Q-table loaded from {filename}")
        except FileNotFoundError:
            print("⚠️ Q-table file not found. Starting from scratch.")

    def get_state(self):
        x, y = self.env.agent_pos

        # Is fire nearby (up/down/left/right)?
        fire_nearby = 0
        for dx, dy in self.actions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.env.size[0] and 0 <= ny < self.env.size[1]:
                if self.env.grid[nx][ny] == 2:
                    fire_nearby = 1
                    break

        # Bucketed distance to nearest exit
        min_dist = min(abs(x - ex[0]) + abs(y - ex[1]) for ex in self.env.exit_positions)
        if min_dist <= 3:
            dist_bucket = 0
        elif min_dist <= 6:
            dist_bucket = 1
        else:
            dist_bucket = 2

        return (x, y, fire_nearby, dist_bucket)

    def get_valid_actions(self, state):
        x, y = state[0], state[1]
        valid = []
        for dx, dy in self.actions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.env.size[0] and 0 <= ny < self.env.size[1]:
                if self.env.grid[nx][ny] in [0, 3]:  # empty or exit
                    valid.append((dx, dy))
        return valid

    def choose_action(self, state):
        valid_actions = self.get_valid_actions(state)
        if not valid_actions:
            return None
        if random.random() < self.epsilon:
            return random.choice(valid_actions)
        q_values = [self.q_table.get((state, a), 0) for a in valid_actions]
        return valid_actions[np.argmax(q_values)]

    def choose_action_test(self, state):
        valid_actions = self.get_valid_actions(state)
        if not valid_actions:
            return None
        q_values = [self.q_table.get((state, a), 0) for a in valid_actions]
        return valid_actions[np.argmax(q_values)]

    def compute_reward(self, state, next_pos):
        # Base reward
        if self.env.grid[next_pos] == 2:
            return -100  # fire
        elif self.env.grid[next_pos] == 3:
            return 100  # exit
        else:
            return -1  # regular step

    def update_q_table(self, state, action, reward, next_state):
        old_q = self.q_table.get((state, action), 0)
        next_valid = self.get_valid_actions(next_state)
        next_max = max([self.q_table.get((next_state, a), 0) for a in next_valid], default=0)
        new_q = old_q + self.alpha * (reward + self.gamma * next_max - old_q)
        self.q_table[(state, action)] = new_q

    def take_action(self, training=True):
        state = self.get_state()
        action = self.choose_action(state) if training else self.choose_action_test(state)
        if action is None:
            return False

        next_pos = (state[0] + action[0], state[1] + action[1])
        reward = self.compute_reward(state, next_pos)
        moved = self.env.move_agent(next_pos)
        next_state = self.get_state()

        if training:
            self.update_q_table(state, action, reward, next_state)

        return moved

