'''Fitness for evaluating the agents results'''
import MalmoPython
import run_simulation
import Fitness
from Fighter import Fighter


runs_per_net = 5

def evaluate_population(genomes, create_func, force_func):
    for g in genomes:
        net = create_func(g)

        fitness = 0

        for runs in range(runs_per_net):
            sim = Fighter()
            fitness += run_simulation(sim, net, force_func)

        # The genome's fitness is its average performance across all runs.
        g.fitness = fitness / float(runs_per_net)



