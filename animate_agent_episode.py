import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
from env.fire_env import FireEscapeEnv
from agents.q_learning_agent import QLearningAgent

# === All configurations ===
configs = [
    ((10, 10), 0.1),
    ((10, 10), 0.3),
    ((10, 10), 0.5),
    ((15, 15), 0.1),
    ((15, 15), 0.3),
    ((15, 15), 0.5)
]

# === Manual color map ===
color_map = {
    0: [1, 1, 1],       # white = empty
    1: [0, 0, 0],       # black = wall
    2: [1, 0, 0],       # red = fire
    3: [0, 1, 0],       # green = exit
    4: [0.2, 0.2, 1],   # blue = agent
}

def grid_to_rgb(grid, agent_pos):
    rgb_image = np.ones((grid.shape[0], grid.shape[1], 3))
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            val = grid[i, j]
            rgb_image[i, j] = color_map.get(val, [1, 1, 1])
    x, y = agent_pos
    rgb_image[x, y] = color_map[4]
    return rgb_image

def animate_one(grid_size, fire_spread):
    name = f"{grid_size[0]}x{grid_size[1]}_fs{int(fire_spread * 10):02}"
    q_table_path = f"results/q_{name}.pkl"
    gif_path = f"results/agent_manual_colors_{name}.gif"

    if not os.path.exists(q_table_path):
        print(f"❌ Skipping {name} — Q-table not found.")
        return

    print(f"🎞 Generating animation for {name}...")

    # Setup environment and agent
    env = FireEscapeEnv(size=grid_size, fire_spread_chance=fire_spread)
    agent = QLearningAgent(env)
    agent.load_q_table(q_table_path)

    # Run and record frames
    frames = []
    status = "stuck"
    for _ in range(100):
        frames.append((env.grid.copy(), env.agent_pos))
        moved = agent.take_action(training=False)
        if not moved:
            status = "stuck"
            break
        if env.is_exit_reached():
            status = "success"
            break
        if env.is_agent_dead():
            status = "fire"
            break
        env.spread_fire()
    frames.append((env.grid.copy(), env.agent_pos))

    # Plot
    fig, ax = plt.subplots(figsize=(6, 6))
    def draw_frame(data):
        grid, agent_pos = data
        ax.clear()
        ax.imshow(grid_to_rgb(grid, agent_pos), interpolation='none')
        ax.set_xticks(np.arange(grid.shape[1]))
        ax.set_yticks(np.arange(grid.shape[0]))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_title(f"Grid {grid_size} - Fire {fire_spread} - {status.upper()}")
        ax.grid(True)
        ax.legend(handles=[
            mpatches.Patch(color='white', label='Empty'),
            mpatches.Patch(color='black', label='Wall'),
            mpatches.Patch(color='red', label='Fire'),
            mpatches.Patch(color='green', label='Exit'),
            mpatches.Patch(color='blue', label='Agent')
        ], loc="upper right", framealpha=0.9)

    ani = animation.FuncAnimation(fig, draw_frame, frames=frames, interval=300)
    ani.save(gif_path, writer="pillow")
    plt.close()
    print(f"✅ Saved: {gif_path}")

# === Run all
for grid_size, fire_spread in configs:
    animate_one(grid_size, fire_spread)
