from stable_baselines import PPO2
import numpy as np
import random




model = PPO2.load('connectx_app/agents_weights/ppo2weight')

print(model, ' :model')

def agent_theo(obs, config):
    # Use the best model to select a column
    col, _ = model.predict(np.array(obs['board']).reshape(6,7,1))
    # Check if selected column is valid
    is_valid = (obs['board'][int(col)] == 0)
    # If not valid, select random move. 
    if is_valid:
        return int(col)
    else:
        return random.choice([col for col in range(config.columns) if obs.board[int(col)] == 0])