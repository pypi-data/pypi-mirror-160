# Abstract interface for a execution strategy
#
# An execution strategy that forms the logic of the experiment.
from masced_bandits.bandit_options import bandit_args
import numpy as np

class Bandit:
    def __init__(self, name):
        self.name = name
        self.last_action = bandit_args["initial_configuration"]

        if(bandit_args['arms']):
            self.arms = bandit_args['arms']
        else:
            print("no arms specified, in Bandit constructor")
            raise RuntimeError("No arms specified")
    def get_next_arm(self, reward):
        """ starts execution """
        pass
    
    def visualize(self):
        """ will create a visualization of the current state of the algorithm """
        pass




