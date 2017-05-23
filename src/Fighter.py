import MalmoPython
import random
import time
import World
import AgentFitness.FitnessBase

'''
Fighter will holds all the definition of what our agents can do
'''

class Fighter:
    def __init__(self, agent_file, neural):
        self.neural = neural
        self.malmo_agent = agent_file
