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
from IPy import IP
from collections import Counter


def SetupClientPools():
    client_pool = MalmoPython.ClientPool()
    num_clients = 0
    if (len(sys.argv) == 1):
        for i in range(2):
            client_pool.add(MalmoPython.ClientInfo('127.0.0.1', 10000+i))
            num_clients += 1
    else:
        clientCounter = Counter(sys.argv[1:])
        for client in clientCounter:
            try:
                IP(str(client))
                for i in range(clientCounter[client]):
                    client_pool.add(MalmoPython.ClientInfo(str(client), 10000+i))
                    num_clients += 1
            except Exception as e:
                print "IP: {} is an invalid address".format(sys.argv[i])

        if num_clients < 2:
            class NotEnoughClientsException(Exception):
                pass
            raise NotEnoughClientsException("Not enough exception passed as a command line argument")
    
    return client_pool, num_clients

def InitalizeNEAT():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-fighter')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path) 
    pop = neat.Population(config)
    return pop, config

if __name__ == "__main__":
    world = World(*SetupClientPools())
    population, config = InitalizeNEAT()
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









