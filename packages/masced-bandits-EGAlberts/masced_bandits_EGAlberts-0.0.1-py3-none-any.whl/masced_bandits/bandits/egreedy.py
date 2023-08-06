from masced_bandits.bandits.Bandit import Bandit
import numpy as np

CUM_REWARD = 0
N_K = 1

class egreedy(Bandit):
    def __init__(self, **kwargs):
        super().__init__("e-greedy")

        self.game_list = []
        self.epsilon = float(kwargs.get('epsilon',0.5))
        self.decay_rate = float(kwargs.get('decay_rate',1.0))

        self.arm_reward_pairs = {}
        for arm in self.arms: self.arm_reward_pairs[arm] = [0.0,0.0]

    def get_next_arm(self, reward):
        self.arm_reward_pairs[self.last_action][CUM_REWARD]+=reward
        self.arm_reward_pairs[self.last_action][N_K]+=1

        choice = np.random.random()

        if(choice < self.epsilon):    
            next_arm = self.arms[np.random.choice(len(self.arms))]
        else:
            next_arm = max(self.arms, key=lambda arm: self.reward_average(arm))

        self.epsilon = self.epsilon/self.decay_rate

        self.last_action = next_arm
        return next_arm

    def reward_average(self, arm):
        return self.arm_reward_pairs[arm][CUM_REWARD] / self.arm_reward_pairs[arm][N_K] if self.arm_reward_pairs[arm][N_K] else 0