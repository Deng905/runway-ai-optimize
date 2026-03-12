"""
main.py - Run All Steps
"""

import os

def run(name, file):
    print(f"\n{'='*40}")
    print(f"▶️  {name}")
    print('='*40)
    os.system(f"python {file}")

if __name__ == "__main__":
    print("🛫 HJJJ Optimization System")
    
    files = [
        ("Airport Model", "airport_data.py"),
        ("Pathfinding", "pathfinder.py"),
        ("Environment", "scheduler_env.py"),
    ]
    
    for name, file in files:
        run(name, file)
    
    ans = input("\n⚠️  Train PPO? (y/n): ")
    if ans == 'y':
        run("Training", "train_ppo.py")
    
    run("Simulation", "simulation.py")
    
    print("\n🎉 COMPLETE!")