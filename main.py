import simulator
from agent.agent import Agent
from simulator.simulator import Simulator
import numpy as np
import matplotlib.pyplot as plt
from planner.planner import Planner


sim_steps = 5
n_agents = 5
radius = 2
height = 10
width = 10
colors = ['b', 'g', 'y', 'r', 'c', 'k']

def create_agent():
    height_list = range(0, height)
    width_list = range(0, width)
    x = np.random.choice(height_list)
    y = np.random.choice(width_list)
    return Agent(state=(x, y), radius=radius, color=colors.pop(0))


if __name__ == "__main__":
    agents = [create_agent() for i in range(0, n_agents)]
    sim = Simulator(agents=agents, height=height, width=width)
    planner = Planner()

    for t in range(0, sim_steps):
        # Draw
        sim.draw()
        plt.pause(0.5)

        # Plan
        planner.plan(agents, n_iters=10)
        # Actuate
        sim.simulate()
