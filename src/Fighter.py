import MalmoPython
import random
import time
import World

'''
Fighter will holds all the definition of what our agents can do
'''

class Fighter:
    def __init__(self, agent_file, neural):
        self.neural = neural
        self.agent = agent_file
        self.ticks = 0
    def isRunning(self):
        return self.agent.getWorldState().is_mission_running
    def run(self):
        self.ticks += 1
        #print(self.cnt)
        output = self.neural.activate(self._get_agent_state_input())
        #print(output)
    def _perform_actions(self, actions):
        pass
    def _get_agent_state_input(self):
        world_state = self.agent.getWorldState()
        if world_state.number_of_observations_since_last_state > 0:
            print(world_state.observations[-1].text)
        return [0 for i in range(31)]
    # def _move_up(self):

    # def _move_down(self):

    # def _move_left(self):

    # def _move_right(self):

    # def _turn_left(self):

    # def _turn_right(self):



