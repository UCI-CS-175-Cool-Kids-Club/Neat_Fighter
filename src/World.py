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
import pickle
from Fighter import Fighter

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
      <ServerQuitFromTimeUp description="" timeLimitMs="20000"/>
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
            <InventoryItem slot="36" type="diamond_helmet" quantity="1" />
            <InventoryItem slot="37" type="diamond_chestplate" quantity="1" />
            <InventoryItem slot="38" type="diamond_leggings" quantity="1" />
            <InventoryItem slot="39" type="diamond_boots" quantity="1" />
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


def GetMission():
    mission_xml = GetMissionXML()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
    return my_mission

class World:
    def __init__(self, client_pool): 
        self.client_pool = client_pool

    def train(self, population):
        i = 0
        while True:
            i += 1
            rt = population.run(self._EvaluateGenome, 5)
            with open('gen-{}'.format(5 * i), 'wb') as f:
                pickle.dump(rt, f)
        return

    def _EvaluateGenome(self, genomes, config):
        for genome_id, genome in genomes:
            print "genome_id: ", genome_id
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
        self.mission = GetMission()
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
