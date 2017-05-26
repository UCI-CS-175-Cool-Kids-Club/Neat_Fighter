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
    pop.add_reporter(neat.Checkpointer(1,900))
    return pop

if __name__ == "__main__":
    world = World(*InitalizeAgents())
    population = InitalizeNEAT()
    world.train(population)



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









