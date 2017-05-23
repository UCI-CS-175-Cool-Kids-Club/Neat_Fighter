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

    def run(self):
        print "Running agent"
        return random.randint(1,20)
