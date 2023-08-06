import numpy as np
from random import sample
from masced_bandits.bandits.Bandit import Bandit
import matplotlib.pyplot as plt



#formula = "ao"
FORMULA_FUNC = None

REWARD = 0
ACTION = 1




class DUCB(Bandit):
    def __init__(self, **kwargs):
        gamma = float(kwargs.get("gamma",0.99))
        super().__init__("DUCB-" + str(gamma))

        self.discount = gamma
        self.bandit_round = -1
        self.game_list = []
        
    def get_next_arm(self, reward):
        self.game_list.append([reward, self.last_action])

        self.bandit_round = self.bandit_round + 1

        if((self.bandit_round) < (len(self.arms))):
            next_arm = self.arms[self.bandit_round]


        else:
            #scores = [str(self.reward_average(arm)) + " c: " + str(self.tuned(arm, sum([self.times_played(arm) for arm in self.arms]))) for arm in self.arms]
            #print("Scores were " + str(scores))
            next_arm = max(self.arms, key=lambda arm: \
                       self.reward_average(arm) + self.tuned(arm, sum([self.times_played(arm) for arm in self.arms])))


        self.last_action = next_arm
        return next_arm


    def reward_average(self, arm):
        r_sum = 0.0
        total_games = len(self.game_list)

        for i, game in enumerate(self.game_list):  
            if(game[ACTION] == arm): #the games in which arm was chosen
                #print("value added to sum: " + str(np.power(self.discount, total_games - i) * game[REWARD]))
                r_sum+=(np.power(self.discount, total_games - i) * game[REWARD])
     
        times_arm_played = self.times_played(arm) 
        if(r_sum == 0 or times_arm_played == 0): return 0
            
        return r_sum/times_arm_played

    
    def sqreward_average(self, arm):
        r_sum = 0.0
        total_games = len(self.game_list)
        for i, game in enumerate(self.game_list):  
            if(game[ACTION] == arm): #the games in which arm was chosen
                r_sum+=np.square(np.power(self.discount, total_games - i) * game[REWARD])

        times_arm_played = self.times_played(arm) 
        if(r_sum == 0 or times_arm_played == 0): return 0
            
        return r_sum/times_arm_played

    def times_played(self, arm):
        arm_played = 0.0
        total_games = len(self.game_list)
        for i, game in enumerate(self.game_list):
            if(game[ACTION] == arm): arm_played += np.power(self.discount, total_games - i) #Each time the g am


        return arm_played


    def tuned(self, arm, n):
        n_k = self.times_played(arm)

        average_of_squares = self.sqreward_average(arm)
        square_of_average = np.square(self.reward_average(arm))
        estimated_variance = average_of_squares - square_of_average
        param = np.log(n) / n_k
        
        V_k = estimated_variance + np.sqrt(2 * param)
        
        #print("values inside tuned " + str((n_k,average_of_squares,square_of_average,estimated_variance,param,V_k)))
        confidence_value = np.sqrt(param * V_k)
        if(np.isnan(confidence_value)):
            print("\n\n\n\ncaught a nan\n\n\n\n\n")
            return 0
        else:
            return confidence_value
    # def visualize(self):
    #     if((self.bandit_round) < (len(self.arms))): return
    #     arm_names = []
    #     arm_rewards= []
    #     arm_conf = []
    #     [(arm_names.append(str(arm)), arm_rewards.append(self.reward_average(arm)), arm_conf.append(self.tuned(arm, sum([self.times_played(arm) for arm in self.arms])))) for arm in self.arms]
    #     reward_bar = plt.bar(arm_names, arm_rewards)
    #     confidence_bar = plt.bar(arm_names, arm_conf, bottom=arm_rewards)
    #     #plt.bar_label(reward_bar, padding=3)
    #     #plt.bar_label(confidence_bar, padding=3)
    #     plt.yticks(np.arange(1.0,3.00, step=0.05))
    #     plt.pause(0.05)
    #     plt.cla()
    #     plt.draw()