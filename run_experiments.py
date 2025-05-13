import os
import csv
from env.fire_env import FireEscapeEnv
from agents.reactive_agent import ReactiveAgent
from agents.search_agent import SearchAgent
from agents.q_learning_agent import QLearningAgent

EPISODES = 30
FIRE_SPREAD_VALUES = [0.1, 0.3, 0.5]
GRID_SIZES = [(10, 10), (15, 15)]
AGENTS = ['reactive', 'search', 'q_learning']

def run_episode(agent_type, env):
    if agent_type == 'reactive':
        agent = ReactiveAgent(env)
        get_move = lambda: agent.choose_move()
    elif agent_type == 'search':
        agent = SearchAgent(env)
        get_move = lambda: agent.next_move()
    elif agent_type == 'q_learning':
        agent = QLearningAgent(env)
        q_table_file = f"results/q_{env.size[0]}x{env.size[1]}_fs{int(env.fire_spread_chance * 10):02}.pkl"
        agent.load_q_table(q_table_file)
        get_move = lambda: agent.take_action(training=False)
    else:
        return "invalid"

    for step in range(100):
        if agent_type in ['reactive', 'search']:
            move = get_move()
            if move is None:
                return 'stuck'
            env.move_agent(move)
        else:
            moved = get_move()
            if not moved:
                return 'stuck'

        if env.is_exit_reached():
            return 'success'
        if env.is_agent_dead():
            return 'fire'

        env.spread_fire()

    return 'stuck'

# Run experiments
results = []
for grid_size in GRID_SIZES:
    for fire_spread in FIRE_SPREAD_VALUES:
        for agent_type in AGENTS:
            print(f"🔥 Testing {agent_type.upper()} - Grid: {grid_size}, Fire: {fire_spread}")
            outcome_counts = {'success': 0, 'fire': 0, 'stuck': 0}
            for episode in range(EPISODES):
                env = FireEscapeEnv(size=grid_size, fire_spread_chance=fire_spread)
                outcome = run_episode(agent_type, env)
                outcome_counts[outcome] += 1
            results.append({
                'agent': agent_type,
                'grid': f"{grid_size[0]}x{grid_size[1]}",
                'fire_spread': fire_spread,
                **outcome_counts
            })

# Save results to CSV
csv_file = "results/agent_evaluation.csv"
os.makedirs("results", exist_ok=True)

with open(csv_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['agent', 'grid', 'fire_spread', 'success', 'fire', 'stuck'])
    writer.writeheader()
    writer.writerows(results)

print(f"\n✅ Evaluation complete. Results saved to: {csv_file}")
