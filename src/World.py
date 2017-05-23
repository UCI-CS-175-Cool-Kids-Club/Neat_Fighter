#!/usr/bin/python
'''
Wrapper class for interpreting our world and transforming Malmo's output of the Agent's world into appropriate format
for our algorithm interpretation.
'''

import MalmoPython
import uuid
import sys
import time
import random
import Fitness
from Fighter import Fighter

sys.path.insert(0, '../neat-python')
import neat

class World:
    def __init__(self, client_pool, mission):
        self.client_pool = client_pool
        self.mission = mission
        print

    def train(self, population):
        return population.run(self._EvaluateGenome)

    def _EvaluateGenome(self, genomes, config):
        for genome_id, genome in genomes:
            print genome_id
            agents = [MalmoPython.AgentHost() for x in range(2)]
            self._StartMission(agents)
            neural_net = neat.nn.FeedForwardNetwork.create(genome, config)
            agents_fighter = [Fighter(agents[i], neural_net) for i in range(2)]
            genome.fitness = self._RunFighterParallel(agents_fighter)
            for i in agents:
                del i
            del agents_fighter

    def _RunFighterParallel(self, fighters):
        print("calling move for both agents until done")
        while all([fighter.isRunning() for fighter in fighters]):
            sys.stdout.write(".")
            time.sleep(0.1)
            for fighter in fighters:
                fighter.move()
                for error in fighter.agent.getWorldState().errors:
                    print "Error:",error.text
        #return max(fighter1.run(), fighter2.run())
        return 0 #this should be the fitness or something

    def _StartMission(self, agent_hosts):
        expId = str(uuid.uuid4())
        for i in range(len(agent_hosts)):
            max_retries = 3
            for retry in range(max_retries):
                try:
                    agent_hosts[i].startMission( self.mission, self.client_pool, MalmoPython.MissionRecordSpec(), i, expId )
                    break
                except RuntimeError as e:
                    if retry == max_retries - 1:
                        print "Error starting mission",e
                        print "Is the game running?"
                        exit(1)
                    else:
                        time.sleep(5)

        hasBegun = 0
        hadErrors = False
        while hasBegun < len(agent_hosts) and not hadErrors:
            time.sleep(0.1)
            for ah in agent_hosts:
                world_state = ah.getWorldState()
                if world_state.has_mission_begun:
                    hasBegun+= 1
                if len(world_state.errors):
                    hadErrors = True
                    print "Errors from agent " + agentName(agent_hosts.index(ah))
                    for error in world_state.errors:
                        print "Error:",error.text
        if hadErrors:
            print "ABORTING ERROR DETECTED"
            exit(1)
