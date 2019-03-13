import numpy as np
import time
from joblib import Parallel, delayed
import multiprocessing

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

    def plan_sga(self, agents):
        """
        Performs Sequential Greedy Assignment as a baseline algorithm.
        :param agents: Set of agents to plan for.
        :param radius:
        :return: None
        """
        observed_points = set()
        for agent in agents:
            best_action = []
            best_cost = -1
            best_set = set()
            for succ, action in agent.get_successors():
                succ_best_cost = len(observed_points.union(agent.get_observations(succ)))
                if succ_best_cost > best_cost:
                    best_action = action
                    best_cost = succ_best_cost
                    best_set = agent.get_observations(succ)
            observed_points = observed_points.union(best_set)
            agent.set_next_action(best_action)

    def plan(self, agents, n_iters=10, batch_size=10, radius=3):
        """
        Chooses actions for each agent according to Decentralized Continuous Greedy (DCG).
        :param agents: The set of agents.
        :param n_iters: The number of gradient steps (denoted by T in DCG).
        :param radius: The communication radius of each agent. Determines the neighbor sets.
        :return: None
        """

        # Initialize Y vectors
        n_agents = len(agents)
        n_actions = agents[0].n_actions
        y_init = 1. / n_actions * np.ones((n_actions * n_agents, 1))
        Y_init = [y_init] * n_agents

        for t in range(1, n_iters + 1):
            t1 = time.time()
            for idx, agent in enumerate(agents):

                # approximating the gradient takes by orders of magnitude the most time
                v_i = self.approximate_grad(Y_init[idx], agents, batch_size=10)

                v_ip = self.project_P(v_i, agent_idx=idx, n_actions=n_actions, zero_others=True)

                # Average over other agents
                y_avg = np.average(np.array(Y_init), axis=0)
                Y_init[idx] = self.project_P(y_avg + 1.0 / t * v_ip, agent_idx=idx, n_actions=n_actions)


        # Assign the best actions by Argmax
        for idx, agent in enumerate(agents):
            best_action_idx = np.argmax(Y_init[idx][idx*n_actions : idx * n_actions + n_actions])
            for action_idx, succ_act in enumerate(agent.get_successors()):
                if action_idx == best_action_idx:
                    agent.set_next_action(succ_act[1])


    def approximate_grad(self, x, agents, batch_size=100):
        """
        Approximate the gradient of the multilinear extension F(x).
        :param x: The current probability vector.
        :param agents: The agent set.
        :param batch_size: The batch size.
        :return: The approximate gradient.
        """

        grad = np.zeros_like(x)
        for t in range(0, batch_size):

            # Sample according to x/ \|x \|.
            sample = np.random.binomial(n=1, p=x)  # TODO Ensure that x is a valid PDF
            grad_t = np.zeros_like(x)

            for i in range(0, grad_t.shape[0]):

                sample_c = sample.copy()

                sample_c[i] = 1
                cost_plus = self.check_cost(sample_c, agents)

                sample_c[i] = 0
                cost_minus = self.check_cost(sample_c, agents)

                grad_t[i] = cost_plus - cost_minus

            grad = grad + grad_t

        return grad / batch_size

    def parallel_approximate_grad(self, x, agents, batch_size=100):

        num_cores = multiprocessing.cpu_count()
        grad_ts = Parallel(n_jobs=num_cores, verbose=10)(delayed(self.single_grad_step)(x, agents) for i in range(batch_size))
        return sum(grad_ts) / batch_size


    def single_grad_step(self, x, agents):

        sample = np.random.binomial(n=1, p=x)  # TODO Ensure that x is a valid PDF
        grad_t = np.zeros_like(x)

        for i in range(0, grad_t.shape[0]):

            sample_c = sample.copy()

            sample_c[i] = 1
            cost_plus = self.check_cost(sample_c, agents)

            sample_c[i] = 0
            cost_minus = self.check_cost(sample_c, agents)

            grad_t[i] = cost_plus - cost_minus

        return grad_t



    def check_cost(self, x, agents):
        observed_points = set()
        for num, agent in enumerate(agents):
            actions_prob = x[num * agent.n_actions: num * agent.n_actions + agent.n_actions]
            for idx, succ_act in enumerate(agent.get_successors()):
                if actions_prob[idx] == 1:
                    observed_points = observed_points.union(agent.get_observations(succ_act[0]))
        return len(observed_points)

    def project_P(self, v, agent_idx, n_actions, zero_others=False):
        """
        Projects a vector onto the probability Polyhedron.
        :param v: The vector to project.
        :param agent_idx: The index of the agent's Polyhedron.
        :param n_actions: Number of actions per agent.
        :return: The projected vector.
        """
        v_agent = v[agent_idx * n_actions: agent_idx * n_actions + n_actions]
        v_agent = 1.0 / np.sum(v_agent) * v_agent
        projection = v.copy()
        if zero_others:
            projection = np.zeros_like(v)
        projection[agent_idx * n_actions: agent_idx * n_actions + n_actions] = v_agent
        return projection


if __name__ == "__main__":
    planner = Planner()
    v = 1.0 * np.array([1000, 500, 50, 100, 100])
    v = np.hstack((v, v))
    print('Vector', v, 'Projection=', planner.project_P(v, 1, 5))
