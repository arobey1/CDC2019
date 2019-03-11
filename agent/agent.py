import matplotlib.patches as patch
from agent.observation_model import ObservationModel


class Agent(object):

    def __init__(self, state, radius, color='b'):
        self.state = state
        self.radius = radius

        # Action Space
        self.actions = {'stay': (0, 0), 'up': (0, 1), 'down': (0, -1),
                        'left': (-1, 0), 'right': (1, 0)}

        self.next_action = 'stay'
        # self.next_action = 'up'  # To Move Up, uncomment this

        # Observation Model
        self.observation_model = ObservationModel(int(radius/2), res=1)

        # Plotting
        self.color = color
        center = self.motion_model(self.state, [-self.radius/2, -self.radius/2])
        self.patch = patch.Rectangle(xy=center, width=self.radius, height=self.radius, color=self.color)
        obs_points = self.observation_model.get_observed_points(self.state)
        self.obs_patches = [patch.Rectangle(xy=point, width=0.1, height=0.1, color='k') for point in obs_points]

    def get_successors(self):
        """
        Returns possible subsequent states along each valid action, given the current state.
        :return: The list of subequent states.
        """
        return [(self.motion_model(self.state, action), name) for name, action in self.actions.items()]

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
        self.update_patches()

    def update_patches(self):
        '''
        Updates the drawing of the field of view and observed points.
        :return: None
        '''
        # Update the Center of the Observable Square
        center = self.motion_model(self.state, [-self.radius/2, -self.radius/2])
        self.patch.xy = center
        # Update the observed points drawing.
        obs_points = self.observation_model.get_observed_points(self.state)
        for obs_point, patch in zip(obs_points, self.obs_patches):
            patch.xy = obs_point
        # self.obs_patches = [patch.Rectangle(xy=point, width=0.1, height=0.1, color='k') for point in obs_points]

    def motion_model(self, state, action):
        '''
        Applies the motion model x_{t+1} = x_t + u_t, i.e. a discrete time control-additive motion model.
        :param state: The current state at time t.
        :param action: The current action at time t.
        :return: The resulting state x_{t+1}
        '''
        return state[0] + action[0], state[1] + action[1]
