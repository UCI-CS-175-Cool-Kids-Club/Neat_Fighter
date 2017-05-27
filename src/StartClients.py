#!/usr/bin/python

import MalmoPython
import random
from World import World#, GetMission
import os
import sys
sys.path.insert(0, '../neat-python')
import neat
import pickle
import visualize


def SetupClientPools():
    client_pool = MalmoPython.ClientPool()
    for x in xrange(10000, 10000 + 2):
        client_pool.add(MalmoPython.ClientInfo('127.0.0.1', x))
    return client_pool

def InitalizeAgents():
    #my_mission = GetMission()
    client_pool = SetupClientPools()
    return client_pool#, my_mission

def InitalizeNEAT():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-fighter')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path) 
    pop = neat.Population(config)
    
    
    return pop

if __name__ == "__main__":
    world = World(InitalizeAgents())
    population = InitalizeNEAT()
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.Checkpointer(1,900))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    try:
      winner = world.train(population)
    except KeyboardInterrupt, neat.population.CompleteExtinctionException:
      winner = population.best_genome


    #save the winner stuff starts here
    with open('winner-feedforward', 'wb') as f:
        pickle.dump(winner, f)

    print(winner)
    try:
      visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
      visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")
    except:
      pass
    node_names = {-1: 'x', -2: 'dx', -3: 'theta', -4: 'dtheta', 0: 'control'}

    visualize.draw_net(config, winner, True, node_names=node_names)

    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward.gv")
    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward-enabled.gv", show_disabled=False)
    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward-enabled-pruned.gv", show_disabled=False, prune_unused=True)


    '''
        # Save the winner.
    with open('winner-feedforward', 'wb') as f:
        pickle.dump(winner, f)

    print(winner)

    visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
    visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")

    node_names = {-1: 'x', -2: 'dx', -3: 'theta', -4: 'dtheta', 0: 'control'}
    visualize.draw_net(config, winner, True, node_names=node_names)

    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward.gv")
    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward-enabled.gv", show_disabled=False)
    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward-enabled-pruned.gv", show_disabled=False, prune_unused=True)
    '''









