import simulator
from agent.agent import Agent
from simulator.simulator import Simulator
import numpy as np
import matplotlib.pyplot as plt
from planner.planner import Planner
import time

SIM_STEPS = 5
N_AGENTS = 10
WIDTH = 10
HEIGHT = 10
RADIUS = 2
T = 3

# np.random.seed(1)

def main():
    for rnd_seed in range(1, 5):
        np.random.seed(rnd_seed)
        coverage = trial()
        print(coverage)
        plt.plot(range(SIM_STEPS+1), coverage)

    plt.show()
    plt.pause(1000)




def trial():
    agents = [create_agent() for i in range(0, N_AGENTS)]
    sim = Simulator(agents=agents, height=HEIGHT, width=WIDTH)
    planner = Planner()

    start_time = time.time()
    print('Current Coverage is :', planner.compute_cost(agents))
    coverage = [planner.compute_cost(agents)]
    for t in range(0, SIM_STEPS):
        # sim.draw()
        # plt.pause(0.5)

        planner.plan(agents, n_iters=T)
        # planner.plan_sga(agents)

        sim.simulate()
        print('Current Coverage is :', planner.compute_cost(agents))
        coverage.append(planner.compute_cost(agents))

    print('Simulation time: ', time.time() - start_time)
    # plt.pause(1000)

    return coverage


def create_agent():
    x = np.random.choice(range(0, HEIGHT))
    y = np.random.choice(range(0, WIDTH))
    return Agent(state=(x, y), radius=RADIUS, color=np.random.rand(3))


if __name__ == "__main__":
    main()
