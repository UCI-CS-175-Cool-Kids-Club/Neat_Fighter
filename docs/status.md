---
layout: default
title:  Status
---
## Project Summary:
The goal of our project is to train an agent to fight in a 1v1 scenario. We are using a Neuroevolution algorithm which is a form machine learning that uses evolutionary algorithms to train our neural networks. More specifically we are using a NeuroEvolution of Augmenting Topologies (NEAT) algorithm which was created by Ken Stanley in 2002 while he was at The University of Texas Austin. We use the distance between both agents and the damage inflicted in our fitness function. We want to decrease the distance between the agents, so it learns to get close to the opponent as well as increase the damage it inflicts onto the opponent.

## Approach:
As stated before the NEAT algorithm is a type of genetic algorithm created by Ken Stanley which changes its weight parameters based on the fitness and the diversity among the specimen of each generation by tracking the history. It is trained via a genetic algorithm, a brief overview of a genetic algorithms. First we create a large population of chromosomes N. Each represents a different solution to our problem (killing the opposing agent). We then test each chromosome, assign it a fitness score (score of how will the chromosome did). Select two members from that population, currently we are selecting the chromosomes with the best fitness score. Then we crossover the chromosomes (randomly picking a position in the chromosome then swapping everything after it) and mutate the species. More specifically the NEAT algorithm is a type of genetic algorithm which changes its weight parameters based on the fitness and the diversity among the specimen of each generation by tracking the history via history markers for crossover, it evolves the species to bring about the best in each species via evolution or speciation, and incrementally develops the topology of the structure (adding complexities as it grows).

We used a NEAT python library (https://github.com/CodeReclaimers/neat-python) together with Malmo to teach our agent. To begin we created a 10 x 10 grid made of diamond blocks. We spawn our two agents at the same location and randomize the yaw between 0 and 360. Our world trains the population, evaluates the genomes, and handles the fighter. 

Our fighter class can make four moves, move, strafe, turn, and attack. It decides these commands based on the neural net’s output. We also calculate the angle of our agent with respect to the opponent. The distance between our agent and the opponent as well if we have killed the enemy which would result in the mission ending.

These calculated values are then passed to AgentResult which we use as our fitness function. This assigns a fitness to each genome by giving it a scaled reward for inflicting damage and punishes the agent for elapsed time and the distance between the agent and the enemy.

Our config-fighter file has all the configuration for the NEAT algorithms parameters. 
EXPAND ON ALL THIS

## Evaluation: 

## Remaining Goals and Challenges:


