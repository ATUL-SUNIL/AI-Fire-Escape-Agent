from env.fire_env import FireEscapeEnv
from agents.q_learning_agent import QLearningAgent
import os

def train_q_agent(grid_size=(10, 10), fire_spread=0.3, episodes=100000):
    SUCCESS = 0
    total_reward = 0

    env = FireEscapeEnv(size=grid_size, fire_spread_chance=fire_spread)
    agent = QLearningAgent(env)

    os.makedirs("results", exist_ok=True)

    for episode in range(episodes):
        env.reset()
        episode_reward = 0

        for step in range(100):
            moved = agent.take_action()
            if not moved:
                break
            if env.is_exit_reached():
                SUCCESS += 1
                episode_reward += 100
                break
            if env.is_agent_dead():
                episode_reward -= 100
                break
            episode_reward -= 1
            env.spread_fire()

        total_reward += episode_reward

        if (episode + 1) % 50000 == 0:
            avg_reward = total_reward / (episode + 1)
            print(f"[Episode {episode + 1}] Successes: {SUCCESS} | Avg Reward: {avg_reward:.2f}")

    filename = f"results/q_{grid_size[0]}x{grid_size[1]}_fs{int(fire_spread * 10):02}.pkl"
    agent.save_q_table(filename)
    print(f"\n🎉 Training complete for {grid_size} @ fire={fire_spread} | Successes: {SUCCESS}/{episodes}")
    print(f"✅ Saved Q-table to {filename}")

# Train all 6 configs
if __name__ == "__main__":
    configs = [
        ((10, 10), 0.1),
        ((10, 10), 0.3),
        ((10, 10), 0.5),
        ((15, 15), 0.1),
        ((15, 15), 0.3),
        ((15, 15), 0.5)
    ]
    for grid, fs in configs:
        print(f"\n📦 Training for Grid={grid}, Fire={fs}")
        train_q_agent(grid_size=grid, fire_spread=fs, episodes=1000000)
