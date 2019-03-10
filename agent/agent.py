import matplotlib.patches as patch
from agent.observation_model import ObservationModel


class Agent(object):

    def __init__(self, state, radius, color='b'):
        self.state = state
        self.radius = radius

        # Action Space
        self.actions = {'up': (0, 1), 'down': (0, -1),
                        'left': (-1, 0), 'right': (1, 0), 'stay': (0, 0)}
        self.next_action = 'stay'

        # Observation Model
        self.observation_model = ObservationModel(radius, res=1)

        # Plotting
        self.color = color
        self.patch = patch.Rectangle(xy=self.state, width=self.radius, height=self.radius, color=self.color)

    def get_successors(self):
        """
        Returns possible subsequent states along each valid action, given the current state.
        :return: The list of subequent states.
        """
        return [(self.motion_model(self.state, action), action) for name, action in self.actions.items()]

    def get_observations(self, state):
        """
        Returns the observations at a potential new state.
        :param state: The state to observe from.
        :return: The set of observed points at the new state
        """
        return self.observation_model.get_observed_points(state)

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
        self.state = self.motion_model(self.state, self.actions[self.next_action])
        self.patch.xy = self.state

    def motion_model(self, state, action):
        return state[0] + action[0], state[1] + action[1]
