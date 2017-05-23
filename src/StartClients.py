#!/usr/bin/python

import MalmoPython
import numpy
import time
import random
import uuid
import sys

def StartMission(agent_host, my_mission, my_client_pool, my_mission_record, role, expId):
    max_retries = 3
    for retry in range(max_retries):
        try:
            agent_host.startMission( my_mission, my_client_pool, my_mission_record, role, expId )
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print "Error starting mission",e
                print "Is the game running?"
                exit(1)
            else:
                time.sleep(5)

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
      <ServerQuitFromTimeUp description="" timeLimitMs="60000"/>
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
      <VideoProducer want_depth="false">
        <Width>1024</Width>
        <Height>786</Height>
      </VideoProducer>
    </AgentHandlers>
  </AgentSection>

  <AgentSection mode="Survival">
    <Name>Fighter2</Name>
    <AgentStart>
      <Placement pitch="0" x="''' + str(random.randint(1,20)) + '''" y="1" yaw="''' + str(random.randint(0,360)) + '''" z="''' + str(random.randint(1,20)) + ''' "/>
    </AgentStart>
    <AgentHandlers>
      <ContinuousMovementCommands turnSpeedDegs="360"/>
      <VideoProducer want_depth="false">
        <Width>1024</Width>
        <Height>786</Height>
      </VideoProducer>
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
    agent_hosts = [MalmoPython.AgentHost() for x in range(2)]
    my_mission = GetMission()
    client_pool = SetupClientPools()
    experimentID = str(uuid.uuid4())
    for i in range(len(agent_hosts)):
        StartMission(agent_hosts[i], my_mission, client_pool, MalmoPython.MissionRecordSpec(), i, experimentID)
    
    hasBegun = False
    hadErrors = False
    while not hasBegun and not hadErrors:
        time.sleep(0.1)
        for ah in agent_hosts:
            world_state = ah.getWorldState()
            if world_state.has_mission_begun:
                hasBegun = True
            if len(world_state.errors):
                hadErrors = True
                print "Errors from agent " + agentName(agent_hosts.index(ah))
                for error in world_state.errors:
                    print "Error:",error.text
    if hadErrors:
        print "ABORTING ERROR DETECTED"
        exit(1)

    return agent_hosts

    #Initalize Neural Nets
    print "Mission has started"
    while True:
        time.sleep(20)
        break
        for ah in agent_hosts:
            world_state = ah.getWorldState()
            for error in world_state.errors:
                print "Error:",error.text 
    print()
    print("Mission ended")

if __name__ == "__main__":
    agents = InitalizeAgents()
