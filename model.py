import mesa
import random
import math
from agents import Dog, Human  # Assuming Dog and Human classes are in dog.py
from mesa.datacollection import DataCollector
from reinforcement_learning import RLAgent
import time
import csv
import os

class DogHumanModel(mesa.Model):
    """A model to simulate interactions between dogs and humans."""
    
    def __init__(self, width, height, num_dogs, num_humans, num_of_episodes, neutering_rate, vaccination_rate, weekly_kill_rate, initial_money, seed=None):
        # Set up the grid
        super().__init__(seed=seed)
        self.grid = mesa.space.MultiGrid(width, height, torus=True)

        # Set up data collection
        self.datacollector = DataCollector(
            model_reporters={
                "Neutering Rate": self.get_neutering_rate,
                "Vaccination Rate": self.get_vaccination_rate,
                "Weekly Kill Rate": self.get_weekly_kill_rate,
                "Money": self.get_money,
                "Rabid Humans": self.return_the_rabid_human_agents,
                "Attitude Spending": self.get_attitude_spending
            },
            agent_reporters={"Dogs": "dog"}
        )

        self.money = initial_money

        # Set model parameters
        self.neutering_rate = neutering_rate  # Rate at which dogs are sterilized (per week)
        self.vaccination_rate = vaccination_rate  # Rate at which dogs are vaccinated (per week)
        self.weekly_kill_rate = weekly_kill_rate  # Rate at which dogs are killed (per week)

        self.attitude_spending = 20

        self.num_dogs = num_dogs
        self.num_humans = num_humans

        # Training settings
        self.current_episode = 0
        self.num_training_episodes = num_of_episodes

        self.reward = 0
        self.rate_rewards = []  # To store rates and their rewards


        # Create dogs
        for i in range(num_dogs):

            self.random = random.random()
            age = random.randint(0, 13)
            sex = random.choice(["M", "F"])
            rabid = random.choice([True, False])
            sterilized = random.choice([True, False])
            vaccinated = random.choice([True, False])
            adoptability = random.random()
            bred = random.choice([True, False])
            health_status = random.choice(["healthy", "sick"])
            reproductive_status = random.choice(["active", "inactive"])
            aggression_level = random.randint(0,1)

            x = random.randrange(0, self.grid.width)
            y = random.randrange(0, self.grid.height)

            dog = Dog(self, age, sex, rabid, sterilized, vaccinated, adoptability, bred, health_status, (x, y), reproductive_status, aggression_level)

            # self.agents.add(dog)  # Add dog to the agent set
            self.grid.place_agent(dog, (x, y))

        # Create humans
        for i in range(num_humans):
            age = random.randint(20, 60)
            sex = random.choice(["M", "F"])
            attitude_towards_dogs = random.randint(0,1)
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)

            human = Human(model=self, age=age, sex=sex, attitude_towards_dogs=attitude_towards_dogs, location=(x, y))

            self.grid.place_agent(human, (x, y))
        
        # Create RL Agent
        self.rl_agent = RLAgent(action_space=[
            "increase_neutering", "decrease_neutering", 
            "increase_vaccination", "decrease_vaccination", 
            "increase_killing", "decrease_killing",
            "increase_attitude_spending", "decrease_attitude_spending",
            "skip"], 
            state_space=[10, 10, 10, 10, 1], epsilon=0.1, q_table="qtable.pickle")
        
        self.step_count = 0
        
        self.train_rl_agent()
    

    def save_q_table(self, filename):
        """Save the Q-table to a pickle file after training."""
        self.rl_agent.save_q_table(filename)

    def train_rl_agent(self):
        """Run the training loop for the RL agent."""
        while self.current_episode < self.num_training_episodes:
            print(f"Training episode {self.current_episode + 1}/{self.num_training_episodes}")
            self.run_episode()  # Run one episode of the model
            self.current_episode += 1
            
            if self.current_episode % 100 == 0:  # Every 100 episodes, print the status
                print(f"Episode {self.current_episode}: Total money = {self.money}")
        
        self.save_q_table("qtable.pickle")

    
    def run_episode(self):
        """Run a single training episode."""
        self.reset_model()  # Reset the model for each new episode

        for _ in range(50):  # Each episode has 50 steps
            self.step()  # Take one step in the simulation
        
        
        self.save_episode_summary()  # Save summary data after the episode

        
        optimal_rates = self.get_optimal_rates()
        print("Optimal Neuter Rate:", optimal_rates["neuter_rate"])
        print("Optimal Vaccinate Rate:", optimal_rates["vaccinate_rate"])
        print("Weekly Kill Rate", optimal_rates["kill_rate"])
        print("Highest Reward Achieved:", optimal_rates["reward"])
    

    def save_step_data(self):
        """Save relevant data for each simulation step."""
        # Define the column names (fieldnames) for the step data
        fieldnames = [
            "current_episode", 
            "step_count", 
            "neutering_rate", 
            "vaccination_rate", 
            "weekly_kill_rate", 
            "money", 
            "reward", 
            "dog_population", 
            "rabid_dog_population", 
            "vaccinated_dog_population"
        ]
        
        # Check if the file already exists to avoid writing the header multiple times
        file_exists = os.path.isfile("simulation_results.csv")
        
        # Open the CSV file in append mode ('a')
        with open("simulation_results.csv", "a", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # Write the header only if the file doesn't exist
            if not file_exists:
                writer.writeheader()

            # Write the data for the current step
            writer.writerow({
                "current_episode": self.current_episode,
                "step_count": self.step_count,
                "neutering_rate": self.neutering_rate,
                "vaccination_rate": self.vaccination_rate,
                "weekly_kill_rate": self.weekly_kill_rate,
                "money": self.money,
                "reward": self.reward,
                "dog_population": self.return_the_dog_agents(),
                "rabid_dog_population": self.return_the_rabid_dog_agents(),
                "vaccinated_dog_population": self.return_the_vaccinated_dog_agents()
            })

    
    def save_episode_summary(self):
        """Save summary statistics after each training episode."""
        # Define the fieldnames
        fieldnames =  [
            "current_episode", 
            "neutering_rate", 
            "vaccination_rate", 
            "weekly_kill_rate", 
            "money", 
            "reward", 
            "optimal_rates", 
            "dog_population", 
            "rabid_dog_population", 
            "vaccinated_dog_population"
        ]

        # Check if the file already exists to avoid rewriting the header
        file_exists = os.path.isfile("episode_summary.csv")

        # Open the file in append mode ('a')
        with open("episode_summary.csv", "a", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write the header only if the file does not exist
            if not file_exists:
                writer.writeheader()

            # Write the data row for the current episode
            writer.writerow({
                "current_episode": self.current_episode,
                "neutering_rate": self.neutering_rate,
                "vaccination_rate": self.vaccination_rate,
                "weekly_kill_rate": self.weekly_kill_rate,
                "money": self.money,
                "reward": self.reward,
                "optimal_rates": self.get_optimal_rates()["reward"],  # Final reward after episode
                "dog_population": self.return_the_dog_agents(),  # Final dog population
                "rabid_dog_population": self.return_the_rabid_dog_agents(),  # Final rabid dogs
                "vaccinated_dog_population": self.return_the_vaccinated_dog_agents()  # Final vaccinated dogs
            })


    def step(self):
        self.datacollector.collect(self)

        self.step_count += 1

        self.save_step_data()

        self.deduct_spending()

        if self.money <= 0:
            self.reward -= 10000000
            self.rate_rewards.append((self.neutering_rate, self.vaccination_rate, self.weekly_kill_rate, self.reward))
            self.save_episode_summary()  # Save episode data before reset
            self.datacollector.collect(self)
            print("Simulation failed! Retrying!")
            self.running = False
            time.sleep(5)

            self.reset_model()
            self.running = True 

        state = self.get_state()
        action = self.rl_agent.choose_action(tuple(state))

        # Apply the chosen action (adjust rates)
        if self.money > 0:
            self.apply_action(action)

            """Advance the model by one step."""
            self.agents.shuffle_do("step")  # Shuffle and step through agents in random order

            # Evaluate the reward based on the new system state
            self.reward = self.get_reward()
            self.rate_rewards.append((self.neutering_rate, self.vaccination_rate, self.weekly_kill_rate, self.reward))
            next_state = self.get_state()  # Get the state after the action
            self.rl_agent.update_q_table(tuple(state), action, self.reward, tuple(next_state))
        else:
            print("Insufficient funds, skipping agent action.")
            self.neutering_rate = 0
            self.weekly_kill_rate = 0
            self.vaccination_rate = 0
            self.attitude_spending = 0
            # self.reset_model()
    
    def deduct_spending(self):
        """Deduct the money spent on actions each month (regular costs)."""
        # Define a cost factor for each action (e.g., 10x for vaccination and neutering, 1x for killing)
        cost_factors = {
            "neutering": 145,  # 10x cost for neutering
            "vaccination": 35,  # 10x cost for vaccination
            "killing": 25  # 1x cost for killing
        }

        # Calculate the total cost
        self.money -= (
            (self.neutering_rate * cost_factors["neutering"] + 
             self.vaccination_rate * cost_factors["vaccination"] + 
             self.weekly_kill_rate * cost_factors["killing"]) +
             self.attitude_spending
        )

        # Prevent money from going negative
        if self.money < 0:
            self.money = 0  # Prevent going into debt
            print("Insufficient funds! No further actions possible.")


    def apply_action(self, action):
        """Apply the action chosen by the RL agent (adjust the rates)."""

        if action == 0:
            print("Increasing neutering.")
            self.neutering_rate = min(self.neutering_rate + 0.05, 1.0)

        elif action == 1:
            print("Decreasing neutering.")
        
        elif action == 2:
            print("Increasing vaccination.")
            self.vaccination_rate = min(self.vaccination_rate + 0.05, 1.0)
        
        elif action == 3:
            print("Decreasing vaccination.")
            self.vaccination_rate = max(self.vaccination_rate - 0.05, 0.0)
        
        elif action == 4:
            print("Increasing killing.")
            self.weekly_kill_rate = min(self.weekly_kill_rate + 0.05, 1.0)
        
        elif action == 5:
            print("Decreasing killing.")
            self.weekly_kill_rate = max(self.weekly_kill_rate - 0.05, 0.0)
        
        elif action == 6:
            print("Increasing attitude spending.")
            self.attitude_spending = min(self.attitude_spending + 0.05 * self.money, self.money)
            # self.money -= self.attitude_spending
        
        elif action == 7:
            print("Decreasing attitude spending.")
            self.attitude_spending = max(self.attitude_spending + 0.05 * self.money, self.money)

        # If there is not enough money, prevent the action from being applied
        if self.money < 0:
            self.money = 0  # Prevent going into debt
            self.neutering_rate = 0
            self.vaccination_rate = 0
            self.weekly_kill_rate = 0
            self.attitude_spending = 0
            self.attitude_spending_rate = 0
            self.reward = -10000000
            print("Insufficient funds! No action applied.")
    
    def get_optimal_rates(self):
        """Find the rates with the highest reward."""
        optimal = max(self.rate_rewards, key=lambda x: x[2])  # Find the tuple with the highest reward
        print(optimal)
        return {"neuter_rate": optimal[0], "vaccinate_rate": optimal[1], "kill_rate": optimal[2], "reward": optimal[3]}

    def get_state(self):
        """Return the current state of the system for RL agent."""
        num_dogs = self.return_the_dog_agents()
        num_rabid_dogs = self.return_the_rabid_dog_agents()
        num_vaccinated_dogs = self.return_the_vaccinated_dog_agents()
        return [num_dogs, num_rabid_dogs, num_vaccinated_dogs, self.attitude_spending, self.money]

    def get_reward(self):
        """Calculate the reward for the RL agent."""
        # Reward: 
        reward = -0.1 * self.return_the_vaccinated_dog_agents()  # Negative reward for spending money on vaccinations
        reward += 5 * max(0, self.return_the_rabid_dog_agents() - 5)  # Penalty for too many rabid dogs
        reward = -0.1 * self.return_the_rabid_human_agents()
        reward += 10 * (self.money > 100)  # Bonus if government has enough money
        reward -= 10 * self.weekly_kill_rate  # Penalty for high kill rate (reduce over time)

        # Negative reward for insufficient population reduction
        initial_dog_population = self.num_dogs
        if self.return_the_dog_agents() > 0.8 * initial_dog_population:  # If population reduction is less than 20%
            reward -= 50  # Significant penalty for poor reduction

        return reward
    
    def get_agents(self):
        """Return a list of all agents."""
        return self.agents

    def get_agent_by_position(self, position):
        """Return agents at a specific position."""
        return self.grid.get_agents_at(position)
    
    def return_the_dog_agents(self):
        return len([agent for agent in self.agents if isinstance(agent, Dog)])
    
    def return_the_rabid_dog_agents(self):
        return len([agent for agent in self.agents if isinstance(agent,Dog) and agent.rabid==True])
    
    def return_the_vaccinated_dog_agents(self):
        return len([agent for agent in self.agents if isinstance(agent, Dog) and agent.vaccinated==True])
    
    def get_neutering_rate(self):
        return self.neutering_rate

    def get_vaccination_rate(self):
        return self.vaccination_rate

    def get_weekly_kill_rate(self):
        return self.weekly_kill_rate

    def get_money(self):
        return self.money
    
    def return_the_rabid_human_agents(self):
        return len([agent for agent in self.agents if isinstance(agent,Human) and agent.rabid==True])
    
    def get_attitude_spending(self):
        return self.attitude_spending
    
    def reset_model(self):
        self.money = 1000  # Reset money
        self.neutering_rate = 0.1  # Reset neutering rate
        self.vaccination_rate = 0.2  # Reset vaccination rate
        self.weekly_kill_rate = 0.05  # Reset weekly kill rate
        self.attitude_spending = 20
        
        self.remove_all_agents()

        # Create s
        for i in range(self.num_dogs):

            self.random = random.random()
            age = random.randint(0, 13)
            sex = random.choice(["M", "F"])
            rabid = random.choice([True, False])
            sterilized = random.choice([True, False])
            vaccinated = random.choice([True, False])
            adoptability = random.random()
            bred = random.choice([True, False])
            health_status = random.choice(["healthy", "sick"])
            reproductive_status = random.choice(["active", "inactive"])
            aggression_level = random.randint(0,1)

            x = random.randrange(0, self.grid.width)
            y = random.randrange(0, self.grid.height)

            dog = Dog(self, age, sex, rabid, sterilized, vaccinated, adoptability, bred, health_status, (x, y), reproductive_status, aggression_level)

            # self.agents.add(dog)  # Add dog to the agent set
            self.grid.place_agent(dog, (x, y))

        # Create humans
        """
        for i in range(self.num_humans):
            age = random.randint(20, 60)
            sex = random.choice(["M", "F"])
            attitude_towards_dogs = random.randint(0,1)
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)

            human = Human(model=self, age=age, sex=sex, attitude_towards_dogs=attitude_towards_dogs, location=(x, y))

            self.grid.place_agent(human, (x, y))
        """
        
