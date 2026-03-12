"""
scheduler_env.py - PPO Training Environment
"""

import gymnasium as gym
from gymnasium import spaces
import numpy as np
from airport_data import create_hjjj_airport
from pathfinder import find_route


class RunwayEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.G = create_hjjj_airport()
        self.max_queue = 5
        
        self.action_space = spaces.Discrete(self.max_queue + 1)
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0]), 
            high=np.array([5, 300, 1]), 
            dtype=np.float32
        )
        self.reset()
    
    def reset(self, seed=None, options=None):
        self.queue = []
        self.time = 0
        self.delay = 0
        self.completed = 0
        self.runway_busy = 0
        self._add_flight()
        self._add_flight()
        return self._obs(), {}
    
    def _obs(self):
        q_len = len(self.queue)
        avg_wait = np.mean([f['wait'] for f in self.queue]) if q_len > 0 else 0
        busy = 1 if self.time < self.runway_busy else 0
        return np.array([q_len, avg_wait, busy], dtype=np.float32)
    
    def _add_flight(self):
        if len(self.queue) >= self.max_queue:
            return
        start = np.random.choice(['APRON_PAX', 'APRON_CARGO'])
        end = np.random.choice(['HOLD_13', 'HOLD_31'])
        _, taxi_time, _ = find_route(self.G, start, end)
        self.queue.append({'taxi': taxi_time, 'wait': 0})
    
    def step(self, action):
        self.time += 30
        reward = 0
        done = False
        
        for f in self.queue:
            f['wait'] += 30
            self.delay += 30
            reward -= 0.1
        
        runway_free = self.time >= self.runway_busy
        
        if action == 0:
            reward -= 0.5
        else:
            idx = action - 1
            if idx < len(self.queue) and runway_free:
                f = self.queue.pop(idx)
                self.runway_busy = self.time + f['taxi'] + 120
                self.completed += 1
                reward += 10
                if f['wait'] < 60:
                    reward += 5
                self._add_flight()
            elif not runway_free:
                reward -= 5
            else:
                reward -= 2
        
        if np.random.random() < 0.4:
            self._add_flight()
        
        if self.completed >= 50 or self.delay > 5000:
            done = True
        
        return self._obs(), reward, done, False, {}


if __name__ == "__main__":
    print("🤖 Environment Test")
    print("=" * 40)
    env = RunwayEnv()
    obs, _ = env.reset()
    print(f"Obs: {obs}")
    print(f"Actions: {env.action_space.n}")
    
    for i in range(10):
        action = env.action_space.sample()
        obs, reward, done, _, _ = env.step(action)
        if done:
            break
    
    print("✅ Test Complete")