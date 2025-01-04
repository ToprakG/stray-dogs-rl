import numpy as np
import random
import pickle

class RLAgent:
    def __init__(self, action_space, state_space, epsilon=0.1, alpha=0.5, gamma=0.9, q_table=None):
        self.action_space = action_space  # List of discrete actions (increase/decrease for rates)
        self.state_space = state_space  # State space dimensions
        self.epsilon = epsilon  # Exploration rate (epsilon-greedy)
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        
        # Initialize Q-table with zeros
        if q_table:
            with open(q_table, "rb") as f:
                self.q_table = pickle.load(f)
        else:
            self.q_table = {}
    
    def load_q_table(self, filename):
        """Load the Q-table from a pickle file."""
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)
    
    def save_q_table(self, filename):
        """Save the Q-table to a pickle file."""
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)


    def choose_action(self, state):
        """Choose an action based on epsilon-greedy policy."""
        # Convert state to a tuple (indexing format)
        state_idx = tuple(state)

        print(state_idx)

        # Ensure the indices are within bounds
        state_idx = tuple(min(max(s, 0), self.q_table.shape[i] - 1) for i, s in enumerate(state_idx))

        if np.random.rand() < self.epsilon:
            # Explore: Random action
            return np.random.choice(len(self.action_space))
        else:
            # Exploit: Best action based on Q-values
            return np.argmax(self.q_table[state_idx])
    
    def state_to_index(self, state):
        """Convert state tuple to an index for the Q-table."""
        index = []
        for i, s in enumerate(state):
            index.append(min(s, self.state_space[i] - 1))  # Ensure the state value is within bounds
        return tuple(index)


    def update_q_table(self, state, action, reward, next_state):
        """Update the Q-table based on the action taken and the received reward."""
        
        # Clamp state values to be within bounds (0-9)
        state_idx = tuple(min(max(s, 0), self.q_table.shape[i] - 1) for i, s in enumerate(state))

        print(next_state)
        
        # Ensure next_state values are within bounds
        next_state_idx = tuple(min(max(s, 0), self.q_table.shape[i] - 1) for i, s in enumerate(next_state))

        print(next_state_idx)

        next_state_idx_sigma = next_state_idx[:3] + (round(next_state_idx[3]),) + next_state_idx[4:]

        print(next_state_idx_sigma)
        # Get the best action for the next state
        best_next_action = np.argmax(self.q_table[next_state_idx_sigma])
        
        # Get the current Q-value
        current_q_value = self.q_table[state_idx][action]
        
        # Get the future Q-value from the best next action
        future_q_value = self.q_table[next_state_idx_sigma][best_next_action]
        
        # Q-learning update rule
        new_q_value = current_q_value + self.alpha * (reward + self.gamma * future_q_value - current_q_value)
        
        # Update the Q-table
        self.q_table[state_idx][action] = new_q_value

