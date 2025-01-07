from model import DogHumanModel
import pandas as pd
import matplotlib.pyplot as plt
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("--height", type=int, default=10, help="Initial height")
parser.add_argument("--width", type=int, default=10, help="Initial width")
parser.add_argument("--dog_population_size", type=int, default=10, help="Initial dog population size(defualt: 10)")
parser.add_argument("--human_population_size", type=int, default=30, help="Initial human population (default: 30)")
parser.add_argument("--initial_money", type=int, default=1000, help="Initial budget (default 1000)")
parser.add_argument("--num_of_episodes", type=int, default=2, help="Number of training episodes")


args = parser.parse_args()


# Instantiate the model with the necessary parameters
model = DogHumanModel(
    width=args.width, 
    height=args.height, 
    num_dogs=args.dog_population_size, 
    num_humans=args.human_population_size, 
    num_of_episodes=args.num_of_episodes,
    neutering_rate=0.1, 
    vaccination_rate=0.2, 
    weekly_kill_rate=0.05, 
    initial_money=1000, 
    seed=None
)

df = pd.read_csv("simulation_results.csv")


# 1. Reward Over Time
plt.figure(figsize=(10, 6))
plt.plot(df["step_count"], df["reward"], label="Reward", color='blue')
plt.title("Reward Over Time")
plt.xlabel("Step")
plt.ylabel("Reward")
plt.grid(True)
plt.show()

# 2. Dog Population Over Time
plt.figure(figsize=(10, 6))
plt.plot(df["step_count"], df["dog_population"], label="Dog Population", color='orange')
plt.title("Dog Population Over Time")
plt.xlabel("Step")
plt.ylabel("Dog Population")
plt.grid(True)
plt.show()

# 3. Rabid Dog Population Over Time
plt.figure(figsize=(10, 6))
plt.plot(df["step_count"], df["rabid_dog_population"], label="Rabid Dog Population", color='red')
plt.title("Rabid Dog Population Over Time")
plt.xlabel("Step")
plt.ylabel("Rabid Dog Population")
plt.grid(True)
plt.show()

# 4. Vaccinated Dog Population Over Time
plt.figure(figsize=(10, 6))
plt.plot(df["step_count"], df["vaccinated_dog_population"], label="Vaccinated Dog Population", color='green')
plt.title("Vaccinated Dog Population Over Time")
plt.xlabel("Step")
plt.ylabel("Vaccinated Dog Population")
plt.grid(True)
plt.show()

# 5. Neutering, Vaccination, and Killing Rates Over Time
plt.figure(figsize=(10, 6))
plt.plot(df["step_count"], df["neutering_rate"], label="Neutering Rate", color='blue')
plt.plot(df["step_count"], df["vaccination_rate"], label="Vaccination Rate", color='green')
plt.plot(df["step_count"], df["weekly_kill_rate"], label="Killing Rate", color='orange')
plt.title("Rates Over Time")
plt.xlabel("Step")
plt.ylabel("Rate")
plt.legend()
plt.grid(True)
plt.show()

# 6. Money Over Time
plt.figure(figsize=(10, 6))
plt.plot(df["step_count"], df["money"], label="Money", color='purple')
plt.title("Money Over Time")
plt.xlabel("Step")
plt.ylabel("Money")
plt.grid(True)
plt.show()

# 7. Reward vs. Dog Population
plt.figure(figsize=(10, 6))
plt.scatter(df["dog_population"], df["reward"], label="Reward vs Dog Population", alpha=0.5, color='blue')
plt.title("Reward vs Dog Population")
plt.xlabel("Dog Population")
plt.ylabel("Reward")
plt.grid(True)
plt.show()

# 8. Rabid Dogs vs. Vaccinated Dogs
plt.figure(figsize=(10, 6))
plt.scatter(df["vaccinated_dog_population"], df["rabid_dog_population"], label="Vaccinated vs Rabid Dogs", alpha=0.5, color='red')
plt.title("Rabid Dogs vs Vaccinated Dogs")
plt.xlabel("Vaccinated Dog Population")
plt.ylabel("Rabid Dog Population")
plt.grid(True)
plt.show()

# 9. Total Dog Population vs. Reward
plt.figure(figsize=(10, 6))
plt.scatter(df["dog_population"], df["reward"], label="Total Dog Population vs Reward", alpha=0.5, color='green')
plt.title("Total Dog Population vs Reward")
plt.xlabel("Total Dog Population")
plt.ylabel("Reward")
plt.grid(True)
plt.show()

# 10. Rolling Average of Reward Over Time
df['reward_rolling_avg'] = df['reward'].rolling(window=50).mean()
plt.figure(figsize=(10, 6))
plt.plot(df["step_count"], df["reward_rolling_avg"], label="Rolling Average of Reward", color='purple')
plt.title("Rolling Average of Reward Over Time")
plt.xlabel("Step")
plt.ylabel("Reward (Rolling Average)")
plt.grid(True)
plt.show()

# 11. Step vs. Reward
plt.figure(figsize=(10, 6))
plt.plot(df["step_count"], df["reward"], label="Reward per Step", color='blue')
plt.title("Reward per Step Over Time")
plt.xlabel("Step")
plt.ylabel("Reward")
plt.grid(True)
plt.show()