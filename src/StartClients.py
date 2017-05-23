#!/usr/bin/python

import MalmoPython
import numpy
import time
import random

def LoadMission():
    agent_host = MalmoPython.AgentHost()
    mission_file = "../missions/arena.xml"
    with open(mission_file, 'r') as f:
        mission_xml = f.read()
        my_mission = MalmoPython.MissionSpec(mission_xml, True)

# Attempt to start a mission
    try:
        agent_host.startMission(my_mission, MalmoPython.MissionRecordSpec())
    except Exception as e:
        print e
        print("Failed to start mission")
        exit(1)

# Loop until mission starts:
    world_state = agent_host.getWorldState()
    while not world_state.has_mission_begun:
        time.sleep(0.1)
        world_state = agent_host.getWorldState()

# main loop:
    while world_state.is_mission_running:
        time.sleep(0.5)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:",error.text)

    print()
    print("Mission ended")

if __name__ == "__main__":
    LoadMission()
