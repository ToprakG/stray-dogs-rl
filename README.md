# Stray Dog Population Control Simulation

## Overview
This project implements a stray dog population control simulation using the Mesa framework and Reinforcement Learning (RL). The simulation models the dynamics of a stray dog population in an urban environment and explores the effects of various interventions (e.g., sterilization, adoption) on controlling the population over time. This tool aims to provide a platform for studying effective strategies for managing stray animal populations.

## Key Features:
- **Population Dynamics**: Simulates stray dog population growth and the impact of interventions.
- **Reinforcement Learning**: Uses RL to optimize strategies like sterilization and adoption to reduce the population.
- **Intervention Scenarios**: Compares different control strategies (e.g., sterilization, adoption, and combinations).
- **Sensitivity Analysis**: Allows users to experiment with different parameters to see how sensitive the model is to changes in conditions like food availability or intervention rates.

## Installation

### Prerequisites
- Python 3.7+
- Mesa - For agent-based modeling.

### Steps to Install
1. **Clone the repository**:
    ```bash
    git clone https://github.com/ToprakG/stray-dogs-rl.git
    cd stray-dogs-rl
    ```

2. **Create a virtual environment (optional but recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Simulation Model

The model simulates an urban environment where stray dogs interact with the environment and other dogs. The primary agents in this model are stray dogs, whose behavior is influenced by the following factors:
- Population growth (birth rates, death rates, etc.)
- Resource availability (food, shelter)
- Interventions (e.g., sterilization, adoption, culling)
- Reinforcement Learning for optimizing control strategies

The simulation runs for multiple iterations, and data is collected to assess the effectiveness of different intervention strategies in controlling the population size.

### Model Components:
- **Agent (Dog)**: Represents a stray dog in the simulation. Agents interact with the environment and other dogs.
- **Actions**: Dogs can reproduce, seek food, move, and respond to sterilization or adoption interventions.
- **State**: Each dog has attributes like age, health, and location.
- **Environment**: A grid representing the urban area where dogs roam. The environment includes resources like food, shelter, and areas for intervention.

### Interventions:
- **Sterilization**: Dogs are sterilized to prevent reproduction.
- **Adoption**: Stray dogs are adopted into homes.
- **Killing**: Stray dogs are killed.

## Running the Simulation

### Command-Line Interface

1. **Run the simulation with the default settings**:
    ```bash
    python app.py
    ```

2. **Run the simulation with custom parameters**:
    ```bash
    python app.py --width 100 --height 100 --dog_population_size 200 --human_population_size 5000
    ```

   The RL agent returns the most optimized rates for neutering/sterilization and weekly killing.

## Contributing

We welcome contributions to improve and extend this project. If you’d like to contribute, please fork the repository, make changes, and submit a pull request.

### How to Contribute:
1. Fork the repository.
2. Create a new branch for your changes.
3. Make changes and commit them with a meaningful message.
4. Push your branch to your forked repository.
5. Open a pull request from your forked repository to the main repository.

## Citation

This project is licensed under the CC BY-NC 4.0 License - see the LICENSE file for details.

If you use this simulation in your research, please cite it as follows:

```bibtex
@misc{stray-dogs-rl,
  author = {Toprak Gündoğdu},
  title = {Stray Dog Population Control Simulation},
  year = {2025},
  url = {https://github.com/ToprakG/stray-dogs-rl}
}

