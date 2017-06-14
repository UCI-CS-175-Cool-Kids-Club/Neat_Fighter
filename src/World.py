#!/bin/python
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
import pickle
from Fighter import Fighter
from runtime_configs import DEBUGGING
from itertools import izip

sys.path.insert(0, '../neat-python')
import neat

def GetMissionXML():
    mission_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<Mission xmlns="http://ProjectMalmo.microsoft.com" 
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

  <About>
    <Summary>Fighting 1v1</Summary>
  </About>

  <ServerSection>
    <ServerInitialConditions>
            <Time>
                <StartTime>6000</StartTime>
                <AllowPassageOfTime>true</AllowPassageOfTime>
            </Time>
            <Weather>clear</Weather>
            <AllowSpawning>false</AllowSpawning>
    </ServerInitialConditions>
    <ServerHandlers>
      <FlatWorldGenerator generatorString="3;1*minecraft:grass;1" forceReset="1"/>
      <DrawingDecorator>
            <DrawLine type="diamond_block" y1="1" y2="1" x1="0" x2="11" z1="0" z2="0" />
            <DrawLine type="diamond_block" y1="1" y2="1" x1="0" x2="0" z1="0" z2="11" />
            <DrawLine type="diamond_block" y1="1" y2="1" x1="11" x2="11" z1="0" z2="11" />
            <DrawLine type="diamond_block" y1="1" y2="1" x1="0" x2="11" z1="11" z2="11" />

            <DrawLine type="diamond_block" y1="2" y2="2" x1="0" x2="11" z1="0" z2="0" />
            <DrawLine type="diamond_block" y1="2" y2="2" x1="0" x2="0" z1="0" z2="11" />
            <DrawLine type="diamond_block" y1="2" y2="2" x1="11" x2="11" z1="0" z2="11" />
            <DrawLine type="diamond_block" y1="2" y2="2" x1="0" x2="11" z1="11" z2="11" />

            <DrawLine type="diamond_block" y1="3" y2="3" x1="0" x2="11" z1="0" z2="0" />
            <DrawLine type="diamond_block" y1="3" y2="3" x1="0" x2="0" z1="0" z2="11" />
            <DrawLine type="diamond_block" y1="3" y2="3" x1="11" x2="11" z1="0" z2="11" />
            <DrawLine type="diamond_block" y1="3" y2="3" x1="0" x2="11" z1="11" z2="11" />

            <DrawLine type="diamond_block" y1="4" y2="4" x1="0" x2="11" z1="0" z2="0" />
            <DrawLine type="diamond_block" y1="4" y2="4" x1="0" x2="0" z1="0" z2="11" />
            <DrawLine type="diamond_block" y1="4" y2="4" x1="11" x2="11" z1="0" z2="11" />
            <DrawLine type="diamond_block" y1="4" y2="4" x1="0" x2="11" z1="11" z2="11" />
      </DrawingDecorator>  
      <ServerQuitFromTimeUp description="" timeLimitMs="10000"/>
      <ServerQuitWhenAnyAgentFinishes/>
    </ServerHandlers>
  </ServerSection>

  <AgentSection mode="Adventure">
    <Name>Fighter1</Name>
    <AgentStart>
        <Placement pitch="0" x="2" y="1" yaw="''' + str(random.randint(0,360)) + '''" z="2"/>
        <Inventory>
            <InventoryItem slot="0" type="wooden_sword" quantity="1" />
        </Inventory>
    
    </AgentStart>
    <AgentHandlers>
    <ObservationFromFullStats/>
    <ContinuousMovementCommands turnSpeedDegs="360"/> 
      <ObservationFromNearbyEntities>
        <Range name="entities" xrange="10" yrange="1" zrange="10"/>
      </ObservationFromNearbyEntities>
      <ObservationFromGrid>
        <Grid name="floor">
            <min x="-1" y="0" z="-1"/>
            <max x="1" y="0" z="1"/> </Grid>
      </ObservationFromGrid>
    </AgentHandlers>
  </AgentSection>

  <AgentSection mode="Adventure">
    <Name>Fighter2</Name>
    <AgentStart>
        <Inventory>
            <InventoryItem slot="0" type="wooden_sword" quantity="1" />
        </Inventory>
        <Placement pitch="0" x="9" y="1" yaw="''' + str(random.randint(0,360)) + '''" z="9"/>
    </AgentStart>
    <AgentHandlers>
    <ObservationFromFullStats/>
    <ContinuousMovementCommands turnSpeedDegs="360"/> 
      <ObservationFromNearbyEntities>
        <Range name="entities" xrange="10" yrange="1" zrange="10"/>
      </ObservationFromNearbyEntities>
      <ObservationFromGrid>
        <Grid name="floor">
            <min x="-1" y="0" z="-1"/>
            <max x="1" y="0" z="1"/> </Grid>
      </ObservationFromGrid>
    </AgentHandlers>
  </AgentSection>

</Mission> '''
    return mission_xml

def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)

def GetMission():
    mission_xml = GetMissionXML()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
    return my_mission

class World:
    def __init__(self, client_pool): 
        self.client_pool = client_pool
        self.best_genome = None

    def train(self, population):
        i = 0
        while True:
            i += 1
            self.best_genome = population.run(self._EvaluateGenome, 1)
            with open('gen-{}-winner'.format(i), 'wb') as f:
                pickle.dump(self.best_genome, f)
        return self.best_genome

    def StartFight(self,genome1, genome2, config):
        agents, agents_fighter = self._SetupFighters(genome1, genome2, config)
        self._RunFighters(*agents_fighter)

    def _SetupFighters(self, genome1, genome2, config):
        agents = [MalmoPython.AgentHost() for i in range(2)]
        self._StartMission(agents)
        agents_fighter = [Fighter(agents[0], neat.nn.FeedForwardNetwork.create(genome1, config)), Fighter(agents[1], neat.nn.FeedForwardNetwork.create(genome2,config))]
        return agents, agents_fighter

    def _EvaluateGenome(self, genomes, config):
        for genome_id, genome in genomes:
            if (DEBUGGING):
                print "Running genome {}".format(genome_id)
                agents, agents_fighter = self._SetupFighters(genome, self.best_genome)
                genome.fitness = self._RunFighters(*agents_fighter)
                if DEBUGGING:
                    print("printing the genomes")
                    print genome
                del agents
                del agents_fighter

    def _RunFighters(self, fighter1, fighter2):
        while fighter1.isRunning() or fighter2.isRunning():
            fighter1.run()
            fighter2.run()
            time.sleep(0.2)
            for error in fighter1.agent.peekWorldState().errors:
                print "Fighter 1 Error:",error.text
            for error in fighter2.agent.peekWorldState().errors:
                print "Fighter 2 Error:",error.text

        fighter1_damage_inflicted = fighter2.data.get(u'DamageTaken')
        fighter1_damage_taken = fighter1.data.get(u'DamageTaken')
        fighter1_mission_time = fighter1.data.get(u'TotalTime')
        fighter1.fighter_result.SetDamageInflicted(fighter1_damage_inflicted)
        fighter1.fighter_result.SetMissionTime(fighter1_mission_time)
        fighter1.fighter_result.SetDamageTaken(fighter1_damage_taken)
        fighter1_fitness = fighter1.fighter_result.GetFitness()

        return fighter1_fitness

        if DEBUGGING:
            print "fighter_1_Fitness: ", fighter1_fitness
            print "fighter_2_Fitness: ", fighter2_fitness

        return fighter1_fitness, fighter2_fitness

    def _StartMission(self, agent_hosts):
        self.mission = GetMission()
        expId = str(uuid.uuid4())
        for i in range(len(agent_hosts)):
            while True:
                try:
                    agent_hosts[i].startMission(self.mission, self.client_pool, MalmoPython.MissionRecordSpec(), i, expId )
                    break
                except RuntimeError as e:
                    print "Failed to start mission: retrying again in 1 seconds"
                    time.sleep(1)

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
