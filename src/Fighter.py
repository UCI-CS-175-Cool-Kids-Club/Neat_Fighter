import MalmoPython
import random
import time
from runtime_configs import DEBUGGING
import json
from threading import Timer
import math
from AgentResult import AgentResult

#DEBUGGING = World.DEBUGGING #i think there's a better way to do this with env vars or cmd line args or something but *shrug*

def angle(a1,a2,b1,b2):
    rt = math.atan2(b2-a2, b1-a1)
    return rt if rt >= 0 else rt + 2*math.pi

def angle_between_agents(a1,a2,yaw1,b1,b2):
    #print a1, a2, b1, b2, yaw1
    angl = angle(a1,a2,b1,b2)
    relative_angle = angl - yaw1 
    return (2 * math.pi) - ((relative_angle + math.pi)%(2*math.pi))
def scale_state_inputs(state_inputs):
    a, d = state_inputs
    return [scale_angle(a), scale_distance(d)]
def scale_distance(distance):
    return distance/9
def scale_angle(theta):
    return (theta/math.pi) - 1


ACTION_TIME = 0.2

'''
Fighter will holds all the definition of what our agents can do
'''

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
        agent_state_input = self._get_agent_state_input()
        scaled_state_input = scale_state_inputs(agent_state_input)
        output = self.neural.activate(scaled_state_input)
        if DEBUGGING:
            print("angle {:.2f}; dist {:.2f};   move {:.3f}; strafe {:.3f}; turn {:.3f}; attack {:.3f}".format(*(agent_state_input + output)))
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
            
        agent_x, agent_y, agent_yaw = entities[0][u'x'], entities[0][u'z'], math.radians((entities[0][u'yaw'] - 90) % 360)
        if len(entities) > 1:
            other_entities = entities[1:]
            other_entities = [(ent, math.hypot(entities[0][u'x'] - ent[u'x'], entities[0][u'z'] - ent[u'z'])) for ent in other_entities]
            other_entities = sorted(other_entities, key=lambda x: x[1])[0]
            closest_ent_x, closest_ent_y, closest_ent_dist = other_entities[0][u'x'], other_entities[0][u'z'], other_entities[1]
            self.fighter_result.AppendDistance(closest_ent_dist)
            to_return.extend([angle_between_agents(agent_x, agent_y, agent_yaw, closest_ent_x, closest_ent_y), closest_ent_dist])
        else:
            to_return.extend([-1, -1])
        return to_return

    def _perform_actions(self, actions):
        pass

