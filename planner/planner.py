class Planner(object):

    def __init__(self):
        pass

    def plan(self, agents, n_iters=10, radius=3):



        for agent in agents:
            successors = agent.get_successors()
            for succ, action in successors:
                print('Agent has succ:', succ)
                print('With Observatons: ', agent.get_observations(succ))
        

