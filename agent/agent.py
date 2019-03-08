import numpy as np
import matplotlib.patches as patch


class Agent(object):

    def __init__(self, state, radius, color='b'):
        self.state = state
        self.radius = radius
        # Action Space
        self.actions = {'up': np.array([0, 1]), 'down': np.array([0, -1]),
                        'left': np.array([-1, 0]), 'right': np.array([1, 0]), 'stay': np.array([0, 0])}
        self.next_action = 'stay'

        # Plotting
        self.color = color
        self.patch = patch.Rectangle(xy=self.state, width=self.radius, height=self.radius, color=self.color)


    def get_successors(self):
        """
        Returns possible subsequent states along each valid action, given the current state.
        :return: The list of subequent states.
        """
        return [self.state + action for name, action in self.actions.items()]

    def set_next_action(self, action):
        """
        Assign next action.
        :param action: The action to assign
        :return: None
        """
        self.next_action = action

    def apply_next_action(self):
        """
        Applies the next action to modify the agent state.
        :return: None
        """
        self.state += self.actions[self.next_action]
        self.patch.xy = self.state
