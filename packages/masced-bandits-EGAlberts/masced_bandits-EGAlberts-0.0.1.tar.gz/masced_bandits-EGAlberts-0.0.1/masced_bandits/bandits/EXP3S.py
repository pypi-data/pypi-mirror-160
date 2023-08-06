import numpy as np
from random import sample
from masced_bandits.bandit_options import bandit_args
from masced_bandits.utilities import convert_conf, save_to_pickle, calculate_utility
from masced_bandits.bandits.Bandit import Bandit
from masced_bandits.bandits.Expert import Expert
from statistics import mean

ACTION = 0
REWARD = 1
N_K = 2

#ETA = 1


class EXP3S(Bandit, Expert):
    def __init__(self, **kwargs): 
        super().__init__("EXP3S-" + str(kwargs))
        self.weights, self.distribution = self.exp3s_initialize(len(self.arms))
        self.num_arms = len(self.arms)

        #np.random.seed(1337)
        total_count = kwargs["horizon"] 
        self.gamma = 1/total_count
        self.alpha = min(1, np.sqrt( (self.num_arms * np.log(self.num_arms * total_count)) / total_count))
        #alpha is the learning rate, the lower it is the harder the probabilities commit. If you set it too high you will get overflowing weights
        #gamma is the discount factor
        #low gamma entails your new reward has slight influence on weights but the weight affects the dsitribution heavily
        #high gamma entails your new reward influences the weights but the weights don't affect the distribution
        self.distr_func()

        
        
       
    def exp3s_initialize(self, num_arms):
        return [1] * num_arms, []



    def get_next_arm(self, reward):
        #print("received this " + str(reward))

        #print("my distribution is ")
        #print(self.distribution)    
        
        self.update_func(reward, self.last_action) #Update weights

        #print("now my weights are")
        #print(self.weights)
        self.distr_func() #(re-)calculate Pt
        
        #print("now my distribution is ")
        #print(self.distribution)     

        new_action = self.sample_action()
  
        self.last_action = self.arms[new_action]

        return self.arms[new_action]

    def propagate_reward(self, reward, chosen_action):
        self.update_func(reward, chosen_action)

        self.distr_func()

    def distr_func(self):
        # exp(eta * S^_t-1i) / SUMkj=1 exp(eta * S^_t-1j)

        sum_weights = sum(self.weights)


        self.distribution.clear()
        #P_t = 
        self.distribution.extend([(1 - self.gamma) * (weight/sum_weights) + (self.gamma/self.num_arms) for weight in self.weights])


    def update_func(self, reward, chosen_action):
        # print("making new weights")
        # print("the distribution is")
        # print(self.distribution)
        reward_estimates = [0] * len(self.arms)

        chosen_arm_i = self.arms.index(chosen_action)

        reward_estimates[chosen_arm_i] = reward/self.distribution[chosen_arm_i]
        # print("rew estimates")
        # print(reward_estimates)
        sum_prev_weights = sum(self.weights)
        #print("prev weight sum")
        #print(sum_prev_weights)

        #print("prev weights are")
        #print(self.weights)
        for weight_i in range(len(self.weights)):
            prev_weight = self.weights[weight_i]
            #print("gamma is " + str(self.gamma))
            leftside = prev_weight * np.exp(self.gamma * reward_estimates[weight_i] / self.num_arms)
            #print("left side is ")
            #print(leftside)
            rightside = ((np.exp(1) * self.alpha) / self.num_arms) * sum_prev_weights
            #print("alpha is ")
            #print(self.alpha)
            #print("right side is ")
            #print(rightside)
            self.weights[weight_i] = leftside + rightside #new weight


