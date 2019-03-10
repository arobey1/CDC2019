class Planner(object):

    def __init__(self):
        pass

    def compute_cost(self, agents):
        """
        Computes the cost of a given agent configuration.
        :param agents: The set of agents.
        :return: The coverage cost function evaluated at the current agent states.
        """
        observed_points = set()  # Use set unions of the observed points to compute the objective.
        for agent in agents:
            observed_points = observed_points.union(agent.get_observations(agent.state))
        return len(observed_points)

    def plan(self, agents, n_iters=10, radius=3):
        """
        Chooses actions for each agent according to Decentralized Continuous Greedy (DCG).
        :param agents: The set of agents.
        :param n_iters: The number of gradient steps.
        :param radius: The communication radius of each agent. Determines the neighbor sets.
        :return: None
        """
        for agent in agents:
            successors = agent.get_successors()
            for succ, action in successors:
                pass
                # print('Agent has succ:', succ)
                # print('With Observatons: ', agent.get_observations(succ))

        # TODO Implement DCG Here:


