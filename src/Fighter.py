import MalmoPython
import random
import time
import World
import json
from threading import Timer
import math

def angle(a1,a2,b1,b2):
    rt = math.atan2(b1-a1, b2-a2)
    return rt if rt >= 0 else rt + 2*math.pi

def angle_between_agents(a1,a2,yaw1,b1,b2):
    print a1, a2, b1, b2, yaw1
    angl = angle(a1,a2,b1,b2)
    relative_angle = angl - yaw1 
    return relative_angle if relative_angle >= 0 else relative_angle + 2 * math.pi

ACTION_TIME = 0.2

'''
Fighter will holds all the definition of what our agents can do
'''

class Fighter:
    def __init__(self, agent_file, neural):
        self.neural = neural
        self.agent = agent_file

    def isRunning(self):
        return self.agent.peekWorldState().is_mission_running

    def run(self):
        while self.agent.peekWorldState().number_of_observations_since_last_state == 0:
            time.sleep(0.01)
        output = self.neural.activate(self._get_agent_state_input())
        print "Outout neural: ", output

        actions = [self._move_a, self._move_d, self._move_s, self._move_w, self._attack, self._turn_right, self._turn_left]
        for i in range(len(output)):
            actions[i](output[i])

    def _get_agent_state_input(self):
        to_return = []
        world_state = self.agent.getWorldState()

        data = json.loads(world_state.observations[-1].text)
        to_return.extend([ int(i == u'diamond_block') for i in data.get(u'floor')])
        entities = data.get(u'entities')
        agent_x, agent_y, agent_yaw = entities[0][u'x'], entities[0][u'y'], math.radians(entities[0][u'yaw'] % 360)
        to_return.append(agent_yaw)
        if len(entities) > 1:
            other_entities = entities[1:]
            other_entities = [(ent, math.hypot(entities[0][u'x'] - ent[u'x'], entities[0][u'z'] - ent[u'z'])) for ent in other_entities]
            other_entities = sorted(other_entities, key=lambda x: x[1])[0]
            closest_ent_x, closest_ent_y, closest_ent_dist = other_entities[0][u'x'], other_entities[0][u'y'], other_entities[1]
            to_return.extend([angle_between_agents(agent_x, agent_y, agent_yaw, closest_ent_x, closest_ent_y), closest_ent_dist])
        else:
            to_return.extend([-1, -1,-1])
        print to_return
        return to_return

    def _move_w(self, time):
        self.agent.sendCommand("move 1")
        Timer(time, lambda: self.agent.sendCommand("move 0") and t).start()

    def _move_s(self, time):
        self.agent.sendCommand("move -1")
        Timer(time, lambda: self.agent.sendCommand("move 0") and t).start()

    def _move_a(self, time):
        self.agent.sendCommand("strafe -1")
        Timer(time, lambda: self.agent.sendCommand("strafe 0") and t).start()

    def _move_d(self, time):
        self.agent.sendCommand("strafe 1")
        Timer(time, lambda: self.agent.sendCommand("strafe 0") and t).start()

    def _attack(self, time):
        if (time >= 1):
            self.agent.sendCommand("attack 1")
            self.agent.sendCommand("attack 0")

    def _turn_left(self, time):
        self.agent.sendCommand("turn -1")
        Timer(time, lambda: self.agent.sendCommand("turn 0") and t).start()

    def _turn_right(self, time):
        self.agent.sendCommand("turn 1")
        Timer(time, lambda: self.agent.sendCommand("turn 0") and t).start()

    def _perform_actions(self, actions):
        pass

