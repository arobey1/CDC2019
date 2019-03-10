

import matplotlib.pyplot as plt
import matplotlib.patches as patch
import agent

class Simulator(object):

    def __init__(self, agents, height=10, width=10):
        self.agents = agents
        self.height = height
        self.width = width

        # Plotting
        self.fig = plt.figure(1)
        self.ax = self.fig.gca()

        plt.ion()

    def simulate(self, T=1):
        """
        Simulate T timesteps.
        :param T: Number of timesteps to simulate
        :return: None
        """
        for agent in self.agents:
            agent.apply_next_action()


    def compute_cost(self):
        pass

    def draw(self):
        for agent in self.agents:
            self.ax.add_patch(agent.patch)
            [self.ax.add_patch(obs_point) for obs_point in agent.obs_patches]

        self.ax.set_xlim([0, self.width])
        self.ax.set_ylim([0, self.height])

        self.ax.set_title('Multi-Agent Coverage')
        self.ax.set_xlabel('X (m)')
        self.ax.set_ylabel('Y (m)')

