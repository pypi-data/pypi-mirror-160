
import numpy as np
import time
from masced_bandits.utilities import calculate_utility, convert_conf
from masced_bandits.bandit_options import bandit_args
from masced_bandits.bandits.Bandit import Bandit



CUM_REWARD = 0
N_K = 1
class ETC(Bandit):
    def __init__(self, **kwargs):
        super().__init__("ETC")

        self.bandit_round = 0

        self.explore_factor = float(kwargs.get('exploration_rounds',10))

        self.arm_reward_pairs = {}
        for arm in self.arms: self.arm_reward_pairs[arm] = [0.0,0.0]

    def get_next_arm(self, reward):
        self.bandit_round+=1
        self.arm_reward_pairs[self.last_action][CUM_REWARD]+=reward
        self.arm_reward_pairs[self.last_action][N_K]+=1

        if  self.bandit_round <= ((len(self.arms)-1) * self.explore_factor):
            new_action = self.arms[(self.bandit_round % len(self.arms))]
        else: 
            new_action = max(self.arms, key=lambda arm: self.reward_average(arm))

        self.last_action = new_action
        return new_action


    def reward_average(self, arm):
        return self.arm_reward_pairs[arm][CUM_REWARD] / self.arm_reward_pairs[arm][N_K] if self.arm_reward_pairs[arm][N_K] else 0


    

    


