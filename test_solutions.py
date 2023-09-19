import numpy as np
import pandas as pd
import sys, os
import seaborn as sns

# Inserting the path for Evoman library
sys.path.insert(0, 'evoman')
from environment import Environment
from demo_controller import player_controller

# Setting the number of hidden neurons in the neural network for the player controller
n_hidden_neurons = 10

# Check if the simulation should be run in headless mode (no GUI)
headless = True
if headless:
    os.environ["SDL_VIDEODRIVER"] = "dummy"  # Set the environment variable to use a "dummy" video driver (no GUI)

# Initializing the Evoman game environment
env = Environment(experiment_name='specialist experiment',
                  playermode="ai",
                  player_controller=player_controller(n_hidden_neurons),
                  speed="normal",
                  enemymode="static",
                  level=2,
                  randomini='yes')

repetitions = 10  # Number of repetitions (not used in the given code)
path = 'BEST_SOLUTIONS/BestSolutions_enemy{}_EA{}.npy'  # Path template to load best solutions

# Setting the parameters for the tests
n_tests = 5
ngen = 20  # Number of generations (not used in the given code)
algorithms = ['roulette', 'tournament']  # Evolutionary algorithms to test

def fitness(env, individual):
    """
    Return the fitness value of one run of the game for an individual/solution with weights x.
    
    Args:
    - env: The game environment in which the individual will be evaluated.
    - individual: The set of parameters/weights for the neural network controller.
    
    Returns:
    - A tuple containing the fitness score of the individual.
    """
    f, p, e, t = env.play(pcont=individual)
    return (f,)

# Initializing arrays and lists for storing results
bestsol_fit = np.zeros((3, 10, 5))
box_data = pd.DataFrame()
fitnesses = []
enemies = []
run = []
test = []
algorithm = []

count = 0
# Loop over evolutionary algorithms and enemies
for ea in algorithms:
    for enemy in range(1, 4):
        print(count)
        count += 1
        env.update_parameter('enemies', [enemy])
        path_sol = path.format(enemy, ea)
        best_solutions_run = np.load(path_sol)  # Load the best solutions for the current enemy and algorithm
        print(best_solutions_run)

        # Test each of the loaded solutions
        for i, sol in enumerate(best_solutions_run):
            # play environment 5 times for each solution
            for n in range(n_tests):
                fitness_score = fitness(env, sol)[0]
                fitnesses.append(fitness_score)
                enemies.append(enemy)
                run.append(i + 1)
                test.append(n + 1)
                algorithm.append(ea)

# Storing results in a DataFrame
box_data['gain (fitness)'] = fitnesses
box_data['enemy'] = enemies
box_data['run'] = run
box_data['test'] = test
box_data['EA'] = algorithm

print(box_data)

# Save the results to a CSV file
box_data.to_csv('dataframes/individual_gain_dataframe')
