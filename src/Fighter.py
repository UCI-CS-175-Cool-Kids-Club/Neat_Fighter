import MalmoPython
import random
import time
import World
import json
from threading import Timer
import math
from AgentResult import AgentResult

'''
Fighter will holds all the definition of what our agents can do
'''

def angle(a1,a2,b1,b2):
    rt = math.atan2(b1-a1, b2-a2)
    return rt if rt >= 0 else rt + 2*math.pi

def angle_between_agents(a1,a2,yaw1,b1,b2):
    #print a1, a2, b1, b2, yaw1
    angl = angle(a1,a2,b1,b2)
    relative_angle = angl - yaw1 
    return (2 * math.pi) - ((relative_angle + math.pi)%(2*math.pi))

class Fighter:
    def __init__(self, agent_file, neural):
        self.neural = neural
        self.agent = agent_file
        self.fighter_result = AgentResult()
        self.mission_ended = False

    def isRunning(self):
        return not self.mission_ended and self.agent.peekWorldState().is_mission_running

    def run(self):
        while self.agent.peekWorldState().number_of_observations_since_last_state == 0:
            if not self.isRunning():
                return
            time.sleep(0.01)
        output = self.neural.activate(self._get_agent_state_input())

        if self.mission_ended or not self.agent.peekWorldState().is_mission_running:
            return

        self.agent.sendCommand("move {}".format(output[0]))
        self.agent.sendCommand("strafe {}".format(output[1]))
        self.agent.sendCommand("turn {}".format(output[2]))
        self.agent.sendCommand("attack {}".format(0 if output[3] <= 0 else 1))

    def _get_agent_state_input(self):
        to_return = []
        world_state = self.agent.getWorldState()
        data = json.loads(world_state.observations[-1].text)
        entities = data.get(u'entities')
        if data.get(u'PlayersKilled') == 1:
            self.mission_ended = True

        agent_x, agent_y, agent_yaw = entities[0][u'x'], entities[0][u'y'], math.radians(entities[0][u'yaw'] % 360)
        if len(entities) > 1:
            other_entities = entities[1:]
            other_entities = [(ent, math.hypot(entities[0][u'x'] - ent[u'x'], entities[0][u'z'] - ent[u'z'])) for ent in other_entities]
            other_entities = sorted(other_entities, key=lambda x: x[1])[0]
            closest_ent_x, closest_ent_y, closest_ent_dist = other_entities[0][u'x'], other_entities[0][u'y'], other_entities[1]
            self.fighter_result.AppendDistance(closest_ent_dist)
            to_return.extend([angle_between_agents(agent_x, agent_y, agent_yaw, closest_ent_x, closest_ent_y), closest_ent_dist])
        else:
            to_return.extend([0, 0])

        to_return[0] = to_return[0]/math.pi - 1
        to_return[1] = to_return[1]/7 - 1
        return to_return
