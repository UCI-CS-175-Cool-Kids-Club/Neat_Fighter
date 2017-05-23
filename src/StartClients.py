#!/usr/bin/python

import MalmoPython
import random
from World import World
import os
import sys
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
			<DrawLine type="diamond_block" y1="1" y2="1" x1="0" x2="21" z1="0" z2="0" />
			<DrawLine type="diamond_block" y1="1" y2="1" x1="0" x2="0" z1="0" z2="21" />
			<DrawLine type="diamond_block" y1="1" y2="1" x1="21" x2="21" z1="0" z2="21" />
			<DrawLine type="diamond_block" y1="1" y2="1" x1="0" x2="21" z1="21" z2="21" />

			<DrawLine type="diamond_block" y1="2" y2="2" x1="0" x2="21" z1="0" z2="0" />
			<DrawLine type="diamond_block" y1="2" y2="2" x1="0" x2="0" z1="0" z2="21" />
			<DrawLine type="diamond_block" y1="2" y2="2" x1="21" x2="21" z1="0" z2="21" />
			<DrawLine type="diamond_block" y1="2" y2="2" x1="0" x2="21" z1="21" z2="21" />

			<DrawLine type="diamond_block" y1="3" y2="3" x1="0" x2="21" z1="0" z2="0" />
			<DrawLine type="diamond_block" y1="3" y2="3" x1="0" x2="0" z1="0" z2="21" />
			<DrawLine type="diamond_block" y1="3" y2="3" x1="21" x2="21" z1="0" z2="21" />
			<DrawLine type="diamond_block" y1="3" y2="3" x1="0" x2="21" z1="21" z2="21" />

			<DrawLine type="diamond_block" y1="4" y2="4" x1="0" x2="21" z1="0" z2="0" />
			<DrawLine type="diamond_block" y1="4" y2="4" x1="0" x2="0" z1="0" z2="21" />
			<DrawLine type="diamond_block" y1="4" y2="4" x1="21" x2="21" z1="0" z2="21" />
			<DrawLine type="diamond_block" y1="4" y2="4" x1="0" x2="21" z1="21" z2="21" />
	  </DrawingDecorator>  
      <ServerQuitFromTimeUp description="" timeLimitMs="10000"/>
      <ServerQuitWhenAnyAgentFinishes/>
    </ServerHandlers>
  </ServerSection>

  <AgentSection mode="Survival">
    <Name>Fighter1</Name>
    <AgentStart>
      <Placement pitch="0" x="''' + str(random.randint(1,20)) + '''" y="1" yaw="''' + str(random.randint(0,360)) + '''" z="''' + str(random.randint(1,20)) + ''' "/>
    </AgentStart>
    <AgentHandlers>
      <ContinuousMovementCommands turnSpeedDegs="360"/>
      
    </AgentHandlers>
  </AgentSection>

  <AgentSection mode="Survival">
    <Name>Fighter2</Name>
    <AgentStart>
      <Placement pitch="0" x="''' + str(random.randint(1,20)) + '''" y="1" yaw="''' + str(random.randint(0,360)) + '''" z="''' + str(random.randint(1,20)) + ''' "/>
    </AgentStart>
    <AgentHandlers>
      <ContinuousMovementCommands turnSpeedDegs="360"/>
      
    </AgentHandlers>
  </AgentSection>

</Mission> '''
    return mission_xml


def GetMission():
    mission_xml = GetMissionXML()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
    return my_mission

def SetupClientPools():
    client_pool = MalmoPython.ClientPool()
    for x in xrange(10000, 10000 + 2):
        client_pool.add(MalmoPython.ClientInfo('127.0.0.1', x))
    return client_pool

def InitalizeAgents():
    my_mission = GetMission()
    client_pool = SetupClientPools()
    return client_pool, my_mission

def InitalizeNEAT():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-fighter')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path) 
    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))
    return pop

if __name__ == "__main__":
    world = World(*InitalizeAgents())
    population = InitalizeNEAT()
    winner = world.train(population)
