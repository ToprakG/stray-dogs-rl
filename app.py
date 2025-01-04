from model import DogHumanModel
from agents import Dog, Human
from mesa.mesa_logging import DEBUG, log_to_stderr
from mesa.visualization import (
    SolaraViz,
    make_plot_component,
    make_space_component,
    Slider
)

log_to_stderr(DEBUG)

def post_process(ax):
    ax.get_figure().colorbar(ax.collections[0], label="Number of dogs", ax=ax)

# Visualization setup
def agent_portrayal(agent):
    """This function tells the visualization how to draw the agents."""
    portrayal = {}
    if isinstance(agent, Dog):
        portrayal["size"] = 5
        if agent.aggression_level > 0.5:
            portrayal["color"] = "tab:red"
        else:
            portrayal["color"] = "tab:blue"
    elif isinstance(agent, Human):
        portrayal["size"] = 25
        portrayal["color"] = "tab:green"

    return portrayal

# Create the SpaceGraph (same as you already have)
SpaceGraph = make_space_component(agent_portrayal, post_process=post_process)

# Create plots for rates and money
NeuteringRatePlot = make_plot_component("Neutering Rate")
VaccinationRatePlot = make_plot_component("Vaccination Rate")
KillRatePlot = make_plot_component("Weekly Kill Rate")
MoneyPlot = make_plot_component("Money")
HumansWithRabiesPlot = make_plot_component("Rabid Humans")
AttitudeSpendingPlot = make_plot_component("Attitude Spending")

# Define model parameters, including sliders for rates and money
model_params = {
    "width": 10,
    "height": 10,
    "num_dogs": 10,  # Slider for number of dogs
    "num_humans": 30,  # Slider for number of humans
    "neutering_rate": 0.1,  # Slider for neutering rate
    "vaccination_rate": 0.2,  # Slider for vaccination rate
    "weekly_kill_rate": 0.05,  # Slider for weekly kill rate
    "initial_money": 100000,  # Slider for initial money
    "seed": None
}

# Instantiate the model with the necessary parameters
model = DogHumanModel(
    width=10, 
    height=10, 
    num_dogs=10, 
    num_humans=30, 
    neutering_rate=0.1, 
    vaccination_rate=0.2, 
    weekly_kill_rate=0.05, 
    initial_money=100000, 
    seed=None
)

# Visualization setup with additional plot components
page = SolaraViz(
    model,
    components=[
        SpaceGraph,  # The main space visualization
        NeuteringRatePlot,  # Plot for neutering rate
        VaccinationRatePlot,  # Plot for vaccination rate
        KillRatePlot,  # Plot for weekly kill rate
        MoneyPlot,  # Plot for government money
        HumansWithRabiesPlot,
        AttitudeSpendingPlot
    ],
    model_params=model_params,
    name="Stray Dog Simulation",
)

page
