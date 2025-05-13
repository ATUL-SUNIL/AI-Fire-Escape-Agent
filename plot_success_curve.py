import numpy as np
import matplotlib.pyplot as plt
from env.fire_env import FireEscapeEnv
from agents.q_learning_agent import QLearningAgent
import os

GRID_SIZE = (10, 10)
FIRE_SPREADS = [0.1, 0.3, 0.5]
EPISODES = 30

success_rates = []

for fire_spread in FIRE_SPREADS:
    env = FireEscapeEnv(size=GRID_SIZE, fire_spread_chance=fire_spread)
    agent = QLearningAgent(env)
    q_file = f"results/q_{GRID_SIZE[0]}x{GRID_SIZE[1]}_fs{int(fire_spread*10):02}.pkl"
    if os.path.exists(q_file):
        agent.load_q_table(q_file)
    else:
        print(f"No Q-table for fire_spread {fire_spread}. Skipping.")
        continue

    success = 0
    for _ in range(EPISODES):
        env.reset()
        for step in range(100):
            moved = agent.take_action(training=False)
            if not moved:
                break
            if env.is_exit_reached():
                success += 1
                break
            if env.is_agent_dead():
                break
            env.spread_fire()

    success_rate = success / EPISODES
    success_rates.append(success_rate)

plt.plot(FIRE_SPREADS, success_rates, marker="o")
plt.xlabel("Fire Spread Probability")
plt.ylabel("Success Rate")
plt.title(f"Q-Learning Agent Success Rate vs Fire Spread\nGrid {GRID_SIZE}")
plt.ylim(0, 1.1)
plt.grid(True)
plt.show()
