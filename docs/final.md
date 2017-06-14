---
layout: default
title:  Final Report
---

## Video

$Place holder

<iframe width="560" height="315" src="https://www.youtube.com/embed/ND62gIA778U" frameborder="0" allowfullscreen></iframe>

## Project Summary
The foundation of our project is to train an agent to fight in a 1v1 scenario. We would like our bots to evolve to learn to kill the opposing agent. We are using a Neuroevolution algorithm, which is a form of machine learning that uses genetic algorithms to evolve the structure and edge-weights of neural networks. More specifically, we are using the NeuroEvolution of Augmenting Topologies (NEAT) algorithm which was created by Ken Stanley in 2002 while he was at The University of Texas Austin. 

We have been able to train 1 bot to fight now we have expanded on this to train two bots to fight each other. We use the relative distance between both agents and the damage inflicted in our fitness function. We want to decrease the distance between the agents, so it learns to get close to the opponent as well as increase the damage it inflicts onto the opposing opponent.

## Context
As stated before, the NEAT algorithm is a type of genetic algorithm created by Ken Stanley which changes its weight parameters based on the fitness and the diversity among the specimen of each generation by tracking the history.  Although this field of "neuroevolution" (evolving the parameters of a neural net through a genetic, evolutionary algorithm) is old and dates back further than this paper, NEAT introduced the idea of "species" in the population.  
 
The idea of speciation is highly motivated by biological analogues.  Essentially, Stanley, et al. wanted to pursue the biological concept of sexual reproduction and chromosome crossover (where two successful genomes are combined to create a new, hopefully successful genome).  However, this concept proved difficult to implement for neuroevolution, since two equally-successful neural nets may have radically different *structures*, such that chromosome crossover is nonsensical and results in an unsuccessful offspring.  Previous solutions were just to give up on implementing this biologically analogous crossover by only implementing asexual reproduction, or to have the neural net's structure predetermined as a hyperparameter.  But Stanley did not give up.  Ken Stanley is a hardworking, persevering researching, and he (et al.) came up with this idea of speciation - in which genomes in the population are grouped together into species, by a similarity metric.  Only organisms within the same species are selected to mate with each other.


## Approaches

__High Level__<br> 
Before we go into the nitty gritty just wanted to explain how this is broken down. In Part I we explain how we setup our environment and different approaches we used. Part II we go into how we trained both of our agents and walk through the code. Lets get started.

__Part I__<br> 
Environment setup We created our world using Project Malmo we tired running our project on different sized worlds with different setups. 

- _10x10x4 Diamond Block Arena, No Armor_: This was our initial approach we thought if we give our agent a big enough arena. Over multiple generations we would clearly see if our agent is learning or not.

![Environment](pics/10x10_No_Armor.png)

- _10x5x4 Diamond Block Enclosure, No Armor_: This was our second iteration on our environment. We wanted to test out different areas to see how greatly it would affect our agent. Our thought process was the smaller the arena the faster the agent would at first randomly hit the opponent. Which in turn would result in a better agent after the course of multiple generations. 

![Environment2](pics/6x6x4 No Diamond.png)

- _10x5x4 Diamond Block Enclosure, with Armor_: Again we tried making our area smaller for the same reasons stated above. 

Our results after comparing across final generations did not prove our hypothesis. There was no obvious direct correlation between the size of the area and how well our final generation preformed. It should be stated that this was only true at our scale testing. 

![Environment3](pics/6x4_Armor.png)

__Part II Training__<br>
Our fighter class can make four continuous moves: move, strafe, turn, and attack. It decides these commands based on the neural net’s output.  There are two inputs to the neural net: the agent's distance to the other agent, and the agent's angle to the other agent.

```python
    def run(self):
        while self.agent.peekWorldState().number_of_observations_since_last_state == 0:
            if not self.isRunning():
                return
            time.sleep(0.01)

        agent_state_input = self._get_agent_state_input()
        scaled_state_input = scale_state_inputs(agent_state_input)
        output = self.neural.activate(scaled_state_input)

        self.agent.sendCommand("move {}".format(output[0]))
        self.agent.sendCommand("strafe {}".format(output[1]))
        self.agent.sendCommand("turn {}".format(output[2]))
        self.agent.sendCommand("attack {}".format(0 if output[3] <= 0 else 1))
```

These calculated values are then passed to AgentResult which we use as our fitness function. This assigns a fitness to each genome by giving it a scaled reward for inflicting damage and punishes the agent for elapsed time and the distance between the agent and the enemy.

__Fitness__<br>
For each genome, we calculate its fitness or how well it does by taking into considering the following results: mission_time, inflicted damage, distance to the other player, and damage taken. As time goes on in the arena, we want to punish the genome because we favor a specie that kill the other opponent as fast as possible. We also want to reward inflicting damage on the other agent and punish taking damage. Lastly, as a means to encourage begining species to get closer to the other agent, we included the distance in our fitness where the distance area over a period of time will be subtracted from the overall fitness. In order words, a specie that consistently spend its time closer to the other agent will have a smaller distance area hence the punishment will be less.

For each of the variable that we are taking in consideration for our fitness function, it is multiplied by a scaling factor in order to make sure that there is a logical ordering of importance. In our current settings, we rate the importance of the variables in the following way of highest to lowest: inflicted damage, damage taken, mission time, and distance area.

```python
INFLICTED_DAMAGE_SCALE = 2#40
DAMAGE_TAKEN_SCALE = INFLICTED_DAMAGE_SCALE * 0.90
TIME_SCALE = 0.01#1
DISTANCE_SCALE = 0.01#100

```
The reasoning behind this ordering is that we want our agent to fight and deal as much damage as possible. An agent who can deal damage should always be favored over one that does not. Second, we favor agent who takes the least damage. The scale for mission time and distance is equal to each other. However, in the earlier generation, mission time will not play much of a role because no one will be able to kill each other.In those cases, distance will be more of a factor in the final fitness relative to the rest of the generation's popuation. We can also assume that if an agent is consistently dealing damage, its distance is also consistently closer to that of the other agent. Hence our final fitness is computed as follows:

```python
def GetFitness(self):
    return self.inflicted_damage * INFLICTED_DAMAGE_SCALE - (self.mission_time * TIME_SCALE) - (DISTANCE_SCALE * self.distance_area) - (DAMAGE_TAKEN_SCALE * self.damage_taken)
```

 
## NEAT Configuration
 
Our config-fighter file has all the configuration for the NEAT algorithms parameters. We used a population size of 100 with two inputs (relative angle to the enemy and distance) and one hidden input. As of current, we are using relu for our activation function but there are other options available to fine tune the learning process. The neat-python library allows us to specify mutation rate, probabilities of adding or removing an edge or node, aggregation in the neural nets, and much more. 


![NEAT_Config](pics/NEAT_Config_Image.png)

## Evaluation

To evaluate our performance, we run our evolutionary program for 10 hours and see if the final generation has learned to kill the opponent.  So far, we have been unsuccessful at reaching this goal.  In the absence of complete success, we look at our bots' fitness throughout generations and see if there is a positive trend.  So far, we have been lackluster at reaching this goal when our population size was 20.

![fitness_of_ea_org_ovr_time](pics/pop_<100_fitness_each_org.png)

![Running_max_fit_ovr_time](pics/pop_<100_max_fitness_ea_org.png)

![Running_max_fit_ovr_time](pics/pop_<100_max_fitness_over_time.png)

## Improvements 

After increasing the population size to 100 we began to see improvments.

![Progress](pics/18766898_10207011941297448_98452268_o.png)


## References
[Link to a NEAT paper](http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf)

[Evolution Strategies](https://blog.openai.com/evolution-strategies/)


