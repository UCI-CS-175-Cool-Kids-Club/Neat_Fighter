FILENAME = "overnight_log2.txt"

generations = []
with open(FILENAME) as f:
	generation = {'ds': [], 'fs': [], 'summary':dict()}
	for line in f:
		if len(line.split()) == 0:
			continue
		if line.split()[0] == 'Distance':
			generation['ds'].append(line.split()[-1])
		elif line.split()[0] == 'Fitness:':
			generation['fs'].append(line.split()[-1])
		elif line.split()[0] == "******":
			generations.append(generation)
			generation = {'ds': [], 'fs': [], 'summary':dict()}
		elif line.split()[0] == "Population's":
			pass
		else:
			pass

from matplotlib import pyplot as plt

total_fs = reduce(lambda x, y: x + y, (g['fs'] for g in generations), [])

plt.plot(range(len(total_fs)), total_fs)
plt.show()
a = raw_input()
running_best_fs = reduce(lambda x,y: x + [max(x[-1],y)], total_fs,[total_fs[0]])

plt.plot(range(len(running_best_fs)), running_best_fs)
plt.show()