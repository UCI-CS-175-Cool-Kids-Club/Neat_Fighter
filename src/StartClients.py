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
from collections import Counter

def SetupClientPools():
    client_pool = MalmoPython.ClientPool()
    for i in range(2):
        client_pool.add(MalmoPython.ClientInfo('127.0.0.1', 10000+i))
    return client_pool

def InitalizeNeatConfig():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-fighter')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path) 
    return config

def InitalizeNEATPopulation():
    config = InitalizeNeatConfig()
    pop = neat.Population(config)
    return pop, config

if __name__ == "__main__":
    world = World(SetupClientPools())
    if len(sys.argv) >= 3:
        with open(sys.argv[1], 'rb') as g1:
            genome1 = pickle.load(g1)
        with open(sys.argv[2], 'rb') as g2:
            genome2 = pickle.load(g2)
        print "Running {} against {}".format(sys.argv[1], sys.argv[2]);
        fitness = world.StartFight(genome1, genome2, InitalizeNeatConfig())
        print "TARGET: Fitness of {} against {} : {}".format(sys.argv[1], sys.argv[2], fitness)
    else:
        if len(sys.argv) == 2:
            population, config = neat.Checkpointer.restore_checkpoint(str(sys.argv[1])), InitalizeNeatConfig()
        else:
            population, config = InitalizeNEATPopulation()
        population.add_reporter(neat.StdOutReporter(True))
        population.add_reporter(neat.Checkpointer(1,900))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)
        try:
          winner = world.train(population)
        except KeyboardInterrupt, neat.population.CompleteExtinctionException:
          winner = population.best_genome
          print("winner is")
          print(winner)

        #save the winner stuff starts here
        with open('winner-feedforward', 'wb') as f:
            pickle.dump(winner, f)
        print("winner is: ")
        print(winner)
        try:
          visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
          visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")
        except:
          pass
        #pole balancing: node_names = {-1: 'x', -2: 'dx', -3: 'theta', -4: 'dtheta', 0: 'control'}
        node_names = {-1:'angle_to_enemy', -2:'distance_to_enemy', 0:'move', 1:'strafe', 2:'turn', 3:'attack'}
        visualize.draw_net(config, winner, True, node_names=node_names)

        visualize.draw_net(config, winner, view=True, node_names=node_names,
                           filename="winner-feedforward.gv")
        visualize.draw_net(config, winner, view=True, node_names=node_names,
                           filename="winner-feedforward-enabled.gv", show_disabled=False)
        visualize.draw_net(config, winner, view=True, node_names=node_names,
                           filename="winner-feedforward-enabled-pruned.gv", show_disabled=False, prune_unused=True)


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









