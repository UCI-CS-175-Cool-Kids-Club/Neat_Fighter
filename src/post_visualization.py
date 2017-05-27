FILENAME = "overnight_log4.txt"
#non_stochastic <---- long, learned to hit.
#overnight_log <-- short (100ish genomes)
#overnight_log2 <-- good length, 350+ genomes, 21ish generations, actually overnight.
#overnight_log3 <-- 4 generations, 150ish genomes.  don't remember what this was.
#overnight_log4
#overnight_log4b <--- long, static positions, random orientations, chanced upon getting close, never learned to hit.

generations = []
with open(FILENAME) as f:
	generation = {'ds': [], 'fs': [], 'summary':dict()}
	for line in f:
		if len(line.split()) == 0:
			continue
		if line.split()[0] == 'Distance':
			generation['ds'].append(float(line.split()[-1]))
		elif line.split()[0] == 'Fitness:':
			generation['fs'].append(float(line.split()[-1]))
		elif line.split()[0] == "******":
			generations.append(generation)
			generation = {'ds': [], 'fs': [], 'summary':dict()}
		elif line.split()[0] == "Population's":
			pass
		else:
			pass

from matplotlib import pyplot as plt

total_fs = reduce(lambda x, y: x + y, (g['fs'] for g in generations), [])

plt.title("FITNESS OF EACH ORGANISM OVER TIME")
plt.plot(range(len(total_fs)), total_fs)
plt.show()
#a = raw_input()
running_best_fs = reduce(lambda x,y: x + [max(x[-1],y)], total_fs,[total_fs[0]])

plt.title("RUNNING MAXIMUM FITNESS OVER TIME")
plt.plot(range(len(running_best_fs)), running_best_fs)
plt.show()

import numpy as np
median_gen_fs = map(lambda g: np.median(g['fs']), generations[1:])
plt.title("Median fitness of each generation over time")
plt.plot(range(len(median_gen_fs)), median_gen_fs)
plt.show()
