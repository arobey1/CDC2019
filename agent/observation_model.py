
import itertools

class ObservationModel(object):
    '''
    The ObservationModel class models the observable area in an area coverage problem.
    '''

    def __init__(self, radius=1, res=1, height=10, width=10):
        '''
        Constructs the Model.
        :param range: Assumes a square observable area with width and height given by range.
        '''
        self.height = height
        self.width = width
        self.res = res
        self.valid_grid_points = [pt for pt in itertools.product(range(0, self.width+1, self.res), range(0, self.height+1, self.res))]
        self.points = [point for point in itertools.product(range(-radius, radius+1, res), range(-radius,radius+1,res))]

    def get_observed_points(self, state):
        '''
        Given an input state, returns the observed points.
        :param state: The state observing from.
        :return: The set of observed points.
        '''
        # TODO Make this return a set of observed points that excludes any points which are not in the valid map area.
        all_obs_pts = set([self.motion_model(state, point) for point in self.points])
        obs_pts = set([pt for pt in all_obs_pts if pt in self.valid_grid_points])
        return obs_pts

    def motion_model(self, state, action):
        return state[0] + action[0], state[1] + action[1]
