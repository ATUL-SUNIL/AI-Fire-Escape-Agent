


# AI Fire Escape Agent

This project simulates an AI-based agent navigating and escaping a fire-spreading grid environment using multiple intelligent agent strategies.

## Table of Contents

1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Technologies Used](#technologies-used)
4. [Agents Implemented](#agents-implemented)
5. [Usage Guide](#usage-guide)
   - [Training Q-Learning Agent](#training-q-learning-agent)
   - [Running Experiments](#running-experiments)
   - [Generating Animations](#generating-animations)
   - [Interactive Visualisation](#interactive-visualisation)
6. [Results](#results)
7. [Key Findings](#key-findings)
8. [Future Work](#future-work)

---

## Introduction

This project investigates the research question:

**"How do different AI algorithms perform in fire escape scenarios with increasing complexity?"**

A grid-based environment simulates spreading fire while intelligent agents must navigate toward an exit.

---

## Project Structure

AI-Fire-Escape-Agent/
├── agents/ # Agent classes
├── env/ # Fire escape environment
├── results/ # Saved Q-tables, outputs, animations
├── train_q_agent.py # Q-learning batch trainer
├── run_experiments.py # Experiment runner
├── animate_agent_episode.py # Animation generator
├── interactive_agent_comparison.py # Interactive results visualisation
├── plot_success_curve.py # Success vs fire spread plot (optional)
├── README.md # Project documentation

## Technologies Used

- Python 3.10+
- Numpy
- Matplotlib
- Plotly
- Custom-built simulation environment

---

## Agents Implemented

### Reactive Agent
- Simple rule-based movement toward closest exit.
- Avoids immediate hazards.

### Search Agent
- Uses A* algorithm to find shortest safe path to exit.

### Q-Learning Agent
- Model-free reinforcement learning agent trained over thousands of episodes to learn optimal escape behaviour.

---

## Usage Guide

### Training Q-Learning Agent

```bash
python train_q_agent.py
````

This trains Q-learning agents across all grid and fire configurations.

### Running Experiments

```bash
python run_experiments.py
```

Runs experiments for all 3 agents and outputs results to `results/agent_evaluation.csv`.

### Generating Animations

```bash
python animate_agent_episode.py
```

Creates an animation showing an agent navigating the grid as fire spreads.

### Interactive Visualisation

```bash
python interactive_agent_comparison.py
```

Displays an interactive plot comparing success rates of all agents under different conditions.

---

## Results

Results of experiments are stored in:

```
results/agent_evaluation.csv
```

Sample animation:

```
results/agent_manual_colors_10x10_fs03.gif
```

---

## Key Findings

* **A* Search Agent*\* performed best in small grid environments by finding guaranteed shortest paths.
* **Q-Learning Agent** showed good generalisation but required extensive training episodes.
* **Reactive Agent** underperformed due to simplistic rule set.

---

## Future Work

* Introduce diagonal movement options.
* Explore multi-agent cooperation strategies.
* Test larger grid sizes and more complex obstacle layouts.

---



