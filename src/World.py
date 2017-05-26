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
import json
from Fighter import Fighter

sys.path.insert(0, '../neat-python')
import neat

class World:
    def __init__(self, client_pool, mission):
        self.client_pool = client_pool
        self.mission = mission

    def train(self, population):
        return population.run(self._EvaluateGenome)

    def _EvaluateGenome(self, genomes, config):
        for genome_id, genome in genomes:
            agents = [MalmoPython.AgentHost() for x in range(2)]
            self._StartMission(agents)
            neural_net = neat.nn.FeedForwardNetwork.create(genome, config)
            agents_fighter = [Fighter(agents[i], neural_net) for i in range(2)]
            genome.fitness = self._RunFighterParallel(*agents_fighter)
            for i in agents:
                del i
            del agents_fighter

    def _RunFighterParallel(self, fighter1, fighter2):
        while fighter1.isRunning():
            time.sleep(0.2)
            result = fighter1.run()
            for error in fighter1.agent.peekWorldState().errors:
                print "Error:",error.text
            

        while fighter2.agent.peekWorldState().number_of_observations_since_last_state == 0:
            pass

        agent2_world = fighter2.agent.getWorldState()
        agent2_data = json.loads(agent2_world.observations[-1].text)
        #print "Agent 2 data: ", agent2_data
        damage = agent2_data.get(u'DamageTaken')
        mission_time = agent2_data.get(u'TotalTime')
        fighter1.fighter_result.SetInflictedDamage(damage)
        fighter1.fighter_result.SetMissionTime(mission_time)
        fitness = fighter1.fighter_result.GetFitness()
        print "Fitness: ", fitness
        return fitness

    def _StartMission(self, agent_hosts):
        expId = str(uuid.uuid4())
        for i in range(len(agent_hosts)):
            max_retries = 10
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
                world_state = ah.peekWorldState()
                if world_state.has_mission_begun:
                    hasBegun+= 1
                if len(world_state.errors):
                    hadErrors = True
                    print "Errors from agent"
                    for error in world_state.errors:
                        print "Error:",error.text
        if hadErrors:
            print "ABORTING ERROR DETECTED"
            exit(1)
