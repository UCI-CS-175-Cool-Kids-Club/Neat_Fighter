'''Fitness for evaluating the agents results'''
import MalmoPython
import json
import math
from Fighter import Fighter

def GetFitness(fighter):
    pass
    world_state = self.agent.getWorldState()
    data = json.loads(world_state.observations[-1].text)
    entities = data.get(u'entities')
    life = data.get(u'Life')
    damage = data.get(u'DamageTaken')

    if len(entities) > 1:
        other_entities = entities[1:]
        other_entities = [(ent, math.hypot(entities[0][u'x'] - ent[u'x'], entities[0][u'z'] - ent[u'z'])) for ent in other_entities]
        other_entities = sorted(other_entities, key=lambda x: x[1])[0]
        closest_ent_x, closest_ent_y, closest_ent_dist = other_entities[0][u'x'], other_entities[0][u'y'], other_entities[1]
        
    return (damage * 100) + closest_ent_dist
