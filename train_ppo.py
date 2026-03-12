"""
train_ppo.py - Train PPO Agent
"""

from stable_baselines3 import PPO
from scheduler_env import RunwayEnv


print("🤖 Training PPO...")
env = RunwayEnv()

model = PPO("MlpPolicy", env, verbose=1, n_steps=128, batch_size=64, n_epochs=4)

model.learn(total_timesteps=5000)

model.save("hjjj_ppo")

print("✅ Training Complete")
print("💾 Model saved: hjjj_ppo.zip")