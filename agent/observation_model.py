
import itertools

class ObservationModel(object):
    '''
    The ObservationModel class models the observable area in an area coverage problem.
    '''

    def __init__(self, radius=1, res=1):
        '''
        Constructs the Model.
        :param range: Assumes a square observable area with width and height given by range.
        '''
        self.points = [point for point in itertools.product(range(-radius,radius,res), range(-radius,radius,res))]

    def get_observed_points(self, state):
        '''
        Given an input state, returns the observed points.
        :param state: The state observing from.
        :return: The set of observed points.
        '''
        return set([self.motion_model(state, point) for point in self.points])

    def motion_model(self, state, action):
        return state[0] + action[0], state[1] + action[1]
