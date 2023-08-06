import numpy as np
from masced_bandits.bandits.Bandit import Bandit

CUM_REWARD = 0
CUM_SQ_REWARD = 1
N_K = 2

class UCBImproved(Bandit):
    def __init__(self, **kwargs):
        super().__init__("UCB-Improved")
        self.horizon = int(kwargs.get("horizon",100))
        self.removable_arms = [arm for arm in self.arms]
        self.arm_reward_pairs = {}
        for arm in self.arms: self.arm_reward_pairs[arm] = [0.0,0.0,0.0]
        self.delta_m = 1.0

        
        
    def get_next_arm(self, reward):
   
        if(len(self.removable_arms) == 1): 
            #converged
            return self.removable_arms[0]
        
        self.arm_reward_pairs[self.last_action][CUM_REWARD]+=reward
        self.arm_reward_pairs[self.last_action][CUM_SQ_REWARD]+=np.square(reward)
        self.arm_reward_pairs[self.last_action][N_K]+=1
        
        delta_sq = np.square(self.delta_m)

        n_m = np.ceil( (2 * np.log(self.horizon * delta_sq))/ delta_sq )

        for arm in self.removable_arms:
            if self.arm_reward_pairs[arm][N_K] < n_m: 
                #exploring
                self.last_action = arm
                return arm

        fac = np.sqrt(np.log(self.horizon * delta_sq) / (2 * n_m))
    
        pair_avgs = [self.arm_reward_pairs[arm][CUM_REWARD]/self.arm_reward_pairs[arm][N_K] \
                    for arm in self.removable_arms]

        del_boundary = max([pair_avg - fac for pair_avg in pair_avgs])

        del_candidates = []

        for avg_i, arm_avg in enumerate(pair_avgs):

            
            if (arm_avg + fac) < del_boundary:
                del_candidates.append(self.removable_arms[avg_i])

        for candidate in del_candidates: self.removable_arms.remove(candidate) 

        self.delta_m = self.delta_m/2

        return self.get_next_arm(reward)